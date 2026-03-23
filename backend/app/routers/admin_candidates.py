from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.admin import Admin
from app.models.test_session import TestSession
from app.models.candidate_attempt import CandidateAttempt
from app.models.problem import Problem
from app.dependencies.admin import get_current_admin
import secrets
import random

router = APIRouter(prefix="/admin/candidates", tags=["admin-candidates"])

@router.get("/")
async def get_candidates(
    session_id: str,
    db: AsyncSession = Depends(get_db), 
    current_admin: Admin = Depends(get_current_admin)
):
    # Verify session belongs to current_admin
    sess_res = await db.execute(select(TestSession).where(TestSession.id == session_id, TestSession.created_by == current_admin.id))
    if not sess_res.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not authorized to access this session")

    # Fetch attempts with problem details
    result = await db.execute(
        select(CandidateAttempt)
        .options(selectinload(CandidateAttempt.problem))
        .where(CandidateAttempt.session_id == session_id)
        .order_by(desc(CandidateAttempt.submitted_at).nulls_last(), desc(CandidateAttempt.started_at).nulls_last())
    )
    attempts = result.scalars().all()
    
    return [{
        "id": str(a.id),
        "candidate_name": a.candidate_name,
        "candidate_email": a.candidate_email,
        "assigned_problem_id": a.assigned_problem_id,
        "problem_title": a.problem.title if a.problem else None,
        "problem_difficulty": a.problem.difficulty if a.problem else None,
        "status": a.status,
        "score": a.score,
        "passed_cases": a.passed_cases,
        "total_cases": a.total_cases,
        "language": a.language,
        "started_at": a.started_at,
        "submitted_at": a.submitted_at,
        "time_taken_seconds": a.time_taken_seconds
    } for a in attempts]

@router.get("/{attempt_id}")
async def get_candidate_detail(
    attempt_id: str,
    db: AsyncSession = Depends(get_db), 
    current_admin: Admin = Depends(get_current_admin)
):
    result = await db.execute(
        select(CandidateAttempt)
        .options(selectinload(CandidateAttempt.problem), selectinload(CandidateAttempt.session))
        .where(CandidateAttempt.id == attempt_id)
    )
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(status_code=404, detail="Candidate attempt not found")
        
    if attempt.session.created_by != current_admin.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    return {
        "id": str(attempt.id),
        "candidate_name": attempt.candidate_name,
        "candidate_email": attempt.candidate_email,
        "assigned_problem_id": attempt.assigned_problem_id,
        "status": attempt.status,
        "score": attempt.score,
        "passed_cases": attempt.passed_cases,
        "total_cases": attempt.total_cases,
        "language": attempt.language,
        "started_at": attempt.started_at,
        "submitted_at": attempt.submitted_at,
        "time_taken_seconds": attempt.time_taken_seconds,
        "submitted_code": attempt.submitted_code,
        "test_results": attempt.test_results,
        "problem": {
            "id": attempt.problem.id,
            "title": attempt.problem.title,
            "difficulty": attempt.problem.difficulty,
            "description": attempt.problem.description
        } if attempt.problem else None
    }

@router.post("/{attempt_id}/assign-extra")
async def assign_extra_problems(
    attempt_id: str,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    result = await db.execute(
        select(CandidateAttempt)
        .options(selectinload(CandidateAttempt.session))
        .where(CandidateAttempt.id == attempt_id)
    )
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(status_code=404, detail="Candidate attempt not found")
        
    if attempt.session.created_by != current_admin.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    session = attempt.session
    
    attempts_res = await db.execute(
        select(CandidateAttempt.assigned_problem_id)
        .where(
            CandidateAttempt.session_id == session.id,
            CandidateAttempt.candidate_email == attempt.candidate_email
        )
    )
    used_ids = set(attempts_res.scalars().all())
    
    prob_query = select(Problem)
    if session.difficulty_filter != "any":
        prob_query = prob_query.where(Problem.difficulty == session.difficulty_filter)
    probs_res = await db.execute(prob_query)
    all_probs = probs_res.scalars().all()
    
    unused = [p for p in all_probs if p.id not in used_ids]
    
    if len(unused) < 2:
        raise HTTPException(status_code=400, detail=f"Not enough unused problems available (found {len(unused)}, need 2). Seed more problems to assign.")
        
    assigned_problems = random.sample(unused, 2)
    
    new_tokens = []
    for p in assigned_problems:
        candidate_token = secrets.token_hex(16)
        new_attempt = CandidateAttempt(
            session_id=session.id,
            candidate_token=candidate_token,
            candidate_name=attempt.candidate_name,
            candidate_email=attempt.candidate_email,
            assigned_problem_id=p.id
        )
        db.add(new_attempt)
        new_tokens.append(candidate_token)
        
    await db.commit()
    
    return {
        "message": "Successfully assigned 2 extra problems",
        "new_links": new_tokens
    }
