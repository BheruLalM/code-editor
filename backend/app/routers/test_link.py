import secrets
import random
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.models.test_session import TestSession
from app.models.candidate_attempt import CandidateAttempt, AttemptStatus
from app.models.candidate_problem import CandidateProblem, ProblemStatus
from app.models.problem import Problem
from app.services.executor import run_test_cases

router = APIRouter(prefix="/test", tags=["test-link"])

class RegisterRequest(BaseModel):
    candidate_name: str
    candidate_email: EmailStr

class SubmitRequest(BaseModel):
    problem_id: str
    language: str
    code: str

@router.get("/{session_token}")
async def check_test_link(session_token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestSession).where(TestSession.session_token == session_token))
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(404, "Invalid test link")
        
    # Permissive: ignore is_active, expires_at, and max_attempts
    return {
        "is_valid": True,
        "title": session.title,
        "description": session.description,
        "difficulty_filter": session.difficulty_filter,
        "time_limit_minutes": session.time_limit_minutes
    }

@router.post("/apply")
async def apply_candidate(
    data: RegisterRequest, 
    db: AsyncSession = Depends(get_db)
):
    # Check if already registered with this email
    ext_res = await db.execute(
        select(CandidateAttempt).where(CandidateAttempt.candidate_email == data.candidate_email)
    )
    existing = ext_res.scalars().first()
    if existing:
        return {
            "candidate_token": existing.candidate_token,
            "status": existing.status,
            "resume": True
        }

    candidate_token = secrets.token_hex(16)
    attempt = CandidateAttempt(
        candidate_token=candidate_token,
        candidate_name=data.candidate_name,
        candidate_email=data.candidate_email,
        status=AttemptStatus.waiting
    )
    db.add(attempt)
    await db.commit()
    
    return {
        "candidate_token": candidate_token,
        "status": AttemptStatus.waiting,
        "message": "Registration successful. Please wait for an admin to assign your test."
    }

@router.get("/attempt/{candidate_token}")
async def get_attempt(candidate_token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CandidateAttempt)
        .options(
            selectinload(CandidateAttempt.problems).selectinload(CandidateProblem.problem)
        )
        .where(CandidateAttempt.candidate_token == candidate_token)
    )
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(404, "Invalid test link")
        
    if attempt.status == AttemptStatus.waiting:
        return {
            "candidate_name": attempt.candidate_name,
            "status": attempt.status,
            "message": "Waiting for admin to assign problems..."
        }

    if attempt.status == AttemptStatus.registered:
        attempt.status = AttemptStatus.started
        attempt.started_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(attempt)
        
    problems_data = []
    for cp in attempt.problems:
        p = cp.problem
        problems_data.append({
            "id": p.id,
            "title": p.title,
            "difficulty": p.difficulty,
            "description": p.description,
            "constraints": p.constraints,
            "examples": p.examples,
            "starter_code": p.starter_code,
            "visible_test_cases": p.visible_test_cases,
            "tags": p.tags,
            "status": cp.status,
            "submitted_code": cp.submitted_code,
            "score": cp.score,
            "language": cp.language,
            "test_results": cp.test_results
        })
    
    return {
        "candidate_name": attempt.candidate_name,
        "candidate_email": attempt.candidate_email,
        "status": attempt.status,
        "started_at": attempt.started_at,
        "time_limit_minutes": attempt.time_limit_minutes,
        "already_submitted": attempt.status == AttemptStatus.submitted,
        "problems": problems_data,
        "score": attempt.score
    }

@router.post("/attempt/{candidate_token}/submit")
async def submit_attempt_problem(
    candidate_token: str,
    data: SubmitRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(CandidateAttempt)
        .options(selectinload(CandidateAttempt.problems))
        .where(CandidateAttempt.candidate_token == candidate_token)
    )
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(404, "Invalid test link")
        
    if attempt.status == AttemptStatus.submitted:
        raise HTTPException(400, "You have already submitted this test")
    if attempt.status == AttemptStatus.timed_out:
        raise HTTPException(400, "Your time has expired")

    now = datetime.now(timezone.utc)
    if attempt.started_at:
        end_time = attempt.started_at + timedelta(minutes=attempt.time_limit_minutes)
        if now > end_time:
            attempt.status = AttemptStatus.timed_out
            await db.commit()
            raise HTTPException(400, "Your time has expired")

    # Find the specific problem to submit
    cp_res = await db.execute(
        select(CandidateProblem)
        .options(selectinload(CandidateProblem.problem))
        .where(CandidateProblem.attempt_id == attempt.id, CandidateProblem.problem_id == data.problem_id)
    )
    cp = cp_res.scalar_one_or_none()
    if not cp:
        raise HTTPException(404, "Assigned problem not found")

    p = cp.problem
    visible = await run_test_cases(data.code, data.language, p.visible_test_cases, False, p.time_limit_seconds)
    hidden = await run_test_cases(data.code, data.language, p.hidden_test_cases, True, p.time_limit_seconds)
    
    all_results = visible + hidden
    passed = sum(1 for r in all_results if r["passed"])
    total = len(all_results)
    score = round((passed / total) * 100, 2) if total > 0 else 0.0
    
    cp.submitted_code = data.code
    cp.language = data.language
    cp.score = score
    cp.passed_cases = passed
    cp.total_cases = total
    cp.status = ProblemStatus.submitted
    
    hidden_passed = sum(1 for r in hidden if r["passed"])
    cp.test_results = {
        "visible": visible,
        "hidden": [{"case_number": r["case_number"], "passed": r["passed"]} for r in hidden],
        "hidden_passed": hidden_passed,
        "hidden_total": len(hidden)
    }
    
    # Check if all problems are submitted to close the attempt
    all_submitted = all(p.status == ProblemStatus.submitted for p in attempt.problems if p.id != cp.id) and cp.status == ProblemStatus.submitted
    
    if all_submitted:
        attempt.status = AttemptStatus.submitted
        attempt.submitted_at = now
        if attempt.started_at:
            attempt.time_taken_seconds = int((now - attempt.started_at).total_seconds())
        
        # Calculate overall score
        total_score = sum(p.score for p in attempt.problems if p.score is not None)
        attempt.score = round(total_score / len(attempt.problems), 2) if attempt.problems else 0.0

    await db.commit()
    
    return {
        "score": score,
        "passed": passed,
        "total": total,
        "status": cp.status,
        "all_submitted": attempt.status == AttemptStatus.submitted,
        "message": "Problem submitted successfully!"
    }
