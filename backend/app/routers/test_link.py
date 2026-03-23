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
from app.models.candidate_attempt import CandidateAttempt
from app.models.problem import Problem
from app.services.executor import run_test_cases

router = APIRouter(prefix="/test", tags=["test-link"])

class RegisterRequest(BaseModel):
    candidate_name: str
    candidate_email: EmailStr

class SubmitRequest(BaseModel):
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

@router.post("/{session_token}/register")
async def register_candidate(
    session_token: str, 
    data: RegisterRequest, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(TestSession).where(TestSession.session_token == session_token))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(404, "Invalid test link")
        
    # Permissive: ignore is_active, expires_at, and max_attempts checks during registration
        
    # Check existing email
    ext_res = await db.execute(
        select(CandidateAttempt).where(
            CandidateAttempt.session_id == session.id,
            CandidateAttempt.candidate_email == data.candidate_email
        )
    )
    existing = ext_res.scalar_one_or_none()
    if existing:
        if existing.status == "submitted":
            return {
                "candidate_token": existing.candidate_token,
                "problem_id": existing.assigned_problem_id,
                "time_limit_minutes": session.time_limit_minutes,
                "candidate_name": existing.candidate_name,
                "already_submitted": True
            }
        elif existing.status in ["registered", "started"]:
            return {
                "candidate_token": existing.candidate_token,
                "problem_id": existing.assigned_problem_id,
                "time_limit_minutes": session.time_limit_minutes,
                "candidate_name": existing.candidate_name,
                "resume": True
            }

    # Assign problem
    prob_query = select(Problem)
    if session.difficulty_filter != "any":
        prob_query = prob_query.where(Problem.difficulty == session.difficulty_filter)
    probs_res = await db.execute(prob_query)
    all_probs = probs_res.scalars().all()
    
    if not all_probs:
        raise HTTPException(500, "No problems available for this difficulty")
        
    attempts_res = await db.execute(select(CandidateAttempt.assigned_problem_id).where(CandidateAttempt.session_id == session.id))
    used_ids = set(attempts_res.scalars().all())
    
    unused = [p for p in all_probs if p.id not in used_ids]
    assigned = random.choice(unused) if unused else random.choice(all_probs)
    
    candidate_token = secrets.token_hex(16)
    attempt = CandidateAttempt(
        session_id=session.id,
        candidate_token=candidate_token,
        candidate_name=data.candidate_name,
        candidate_email=data.candidate_email,
        assigned_problem_id=assigned.id
    )
    db.add(attempt)
    await db.commit()
    
    return {
        "candidate_token": candidate_token,
        "problem_id": assigned.id,
        "time_limit_minutes": session.time_limit_minutes,
        "candidate_name": data.candidate_name
    }

@router.get("/attempt/{candidate_token}")
async def get_attempt(candidate_token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CandidateAttempt)
        .options(selectinload(CandidateAttempt.session), selectinload(CandidateAttempt.problem))
        .where(CandidateAttempt.candidate_token == candidate_token)
    )
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(404, "Invalid test link")
        
    if attempt.status == "registered":
        attempt.status = "started"
        attempt.started_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(attempt)
        
    p = attempt.problem
    prob_data = {
        "id": p.id,
        "title": p.title,
        "difficulty": p.difficulty,
        "description": p.description,
        "constraints": p.constraints,
        "examples": p.examples,
        "starter_code": p.starter_code,
        "visible_test_cases": p.visible_test_cases,
        "tags": p.tags
    }
    
    return {
        "candidate_name": attempt.candidate_name,
        "candidate_email": attempt.candidate_email,
        "status": attempt.status,
        "started_at": attempt.started_at,
        "time_limit_minutes": attempt.session.time_limit_minutes,
        "already_submitted": attempt.status == "submitted",
        "problem": prob_data,
        "submitted_code": attempt.submitted_code if attempt.status == "submitted" else None,
        "score": attempt.score if attempt.status == "submitted" else None,
        "language": attempt.language if attempt.status == "submitted" else None,
        "test_results": attempt.test_results if attempt.status == "submitted" else None
    }

@router.post("/attempt/{candidate_token}/submit")
async def submit_attempt(
    candidate_token: str,
    data: SubmitRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(CandidateAttempt)
        .options(
            selectinload(CandidateAttempt.session),
            selectinload(CandidateAttempt.problem),
        )
        .where(CandidateAttempt.candidate_token == candidate_token)
    )
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(404, "Invalid test link")
        
    now = datetime.now(timezone.utc)

    # Server-side timer enforcement: candidates must submit before time expires.
    if attempt.started_at:
        end_time = attempt.started_at + timedelta(minutes=attempt.session.time_limit_minutes)
        if now > end_time:
            attempt.status = "timed_out"
            await db.commit()
            raise HTTPException(400, "Your time has expired")
    else:
        # If they never hit the "start" endpoint, start the timer at first submit.
        attempt.status = "started"
        attempt.started_at = now
        await db.commit()

    if attempt.session.expires_at and now > attempt.session.expires_at:
        attempt.status = "timed_out"
        await db.commit()
        raise HTTPException(400, "This test session has expired")

    if attempt.status == "submitted":
        raise HTTPException(400, "You have already submitted this test")
    if attempt.status == "timed_out":
        raise HTTPException(400, "Your time has expired")
        
    p = attempt.problem
    visible = await run_test_cases(data.code, data.language, p.visible_test_cases, False, p.time_limit_seconds)
    hidden = await run_test_cases(data.code, data.language, p.hidden_test_cases, True, p.time_limit_seconds)
    
    all_results = visible + hidden
    passed = sum(1 for r in all_results if r["passed"])
    total = len(all_results)
    score = round((passed / total) * 100, 2) if total > 0 else 0.0
    
    time_taken = None
    if attempt.started_at:
        # Time taken in UTC difference
        time_taken = int((datetime.now(timezone.utc) - attempt.started_at).total_seconds())
        
    attempt.submitted_code = data.code
    attempt.language = data.language
    attempt.score = score
    attempt.passed_cases = passed
    attempt.total_cases = total
    
    hidden_passed = sum(1 for r in hidden if r["passed"])
    attempt.test_results = {
        "visible": visible,
        "hidden": [{"case_number": r["case_number"], "passed": r["passed"]} for r in hidden],
        "hidden_passed": hidden_passed,
        "hidden_total": len(hidden)
    }
    attempt.status = "submitted"
    attempt.submitted_at = datetime.now(timezone.utc)
    attempt.time_taken_seconds = time_taken
    
    await db.commit()
    
    return {
        "score": score,
        "passed": passed,
        "total": total,
        "visible_results": visible,
        "hidden_passed": hidden_passed,
        "hidden_total": len(hidden),
        "time_taken_seconds": time_taken,
        "status": "submitted",
        "message": "Solution submitted successfully!"
    }
