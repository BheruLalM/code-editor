from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.admin import Admin
from app.models.test_session import TestSession
from app.models.candidate_attempt import CandidateAttempt, AttemptStatus
from app.models.candidate_problem import CandidateProblem, ProblemStatus
from app.models.problem import Problem
from app.dependencies.admin import get_current_admin
from pydantic import BaseModel
import secrets
import random

router = APIRouter(prefix="/admin/candidates", tags=["admin-candidates"])

class AssignRequest(BaseModel):
    problem_ids: list[str]
    time_limit_minutes: int

@router.get("/")
async def get_candidates(
    session_id: str | None = None,
    db: AsyncSession = Depends(get_db), 
    current_admin: Admin = Depends(get_current_admin)
):
    query = select(CandidateAttempt).options(selectinload(CandidateAttempt.problems).selectinload(CandidateProblem.problem))
    
    if session_id:
        query = query.where(CandidateAttempt.session_id == session_id)
    else:
        # If no session_id, show all candidates assigned by or waiting for this admin? 
        # For now, let's show all that are NOT in waiting status if they want general list
        query = query.where(CandidateAttempt.status != AttemptStatus.waiting)

    result = await db.execute(query.order_by(desc(CandidateAttempt.created_at)))
    attempts = result.scalars().all()
    
    return [{
        "id": str(a.id),
        "candidate_name": a.candidate_name,
        "candidate_email": a.candidate_email,
        "status": a.status,
        "score": a.score,
        "time_taken_seconds": a.time_taken_seconds,
        "created_at": a.created_at,
        "problems_count": len(a.problems)
    } for a in attempts]

@router.get("/waiting")
async def get_waiting_candidates(
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    result = await db.execute(
        select(CandidateAttempt)
        .where(CandidateAttempt.status == AttemptStatus.waiting)
        .order_by(desc(CandidateAttempt.created_at))
    )
    attempts = result.scalars().all()
    return attempts

@router.post("/{attempt_id}/assign")
async def assign_test(
    attempt_id: str,
    data: AssignRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(CandidateAttempt).where(CandidateAttempt.id == attempt_id))
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(404, "Candidate not found")
    
    if attempt.status != AttemptStatus.waiting:
        raise HTTPException(400, "Candidate is already assigned or has started")

    # Verify problems exist
    prob_res = await db.execute(select(Problem).where(Problem.id.in_(data.problem_ids)))
    found_probs = prob_res.scalars().all()
    if len(found_probs) != len(data.problem_ids):
        raise HTTPException(400, "One or more problem IDs are invalid")

    attempt.status = AttemptStatus.registered
    attempt.time_limit_minutes = data.time_limit_minutes
    attempt.admin_id = current_admin.id

    for p in found_probs:
        cp = CandidateProblem(
            attempt_id=attempt.id,
            problem_id=p.id,
            status=ProblemStatus.assigned
        )
        db.add(cp)
    
    await db.commit()
    return {"message": "Test assigned successfully"}

@router.delete("/{attempt_id}")
async def delete_candidate(
    attempt_id: str,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(CandidateAttempt).where(CandidateAttempt.id == attempt_id))
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(404, "Candidate not found")
    
    await db.delete(attempt)
    await db.commit()
    return {"message": "Candidate deleted successfully"}

@router.get("/{attempt_id}")
async def get_candidate_detail(
    attempt_id: str,
    db: AsyncSession = Depends(get_db), 
    current_admin: Admin = Depends(get_current_admin)
):
    result = await db.execute(
        select(CandidateAttempt)
        .options(
            selectinload(CandidateAttempt.problems).selectinload(CandidateProblem.problem)
        )
        .where(CandidateAttempt.id == attempt_id)
    )
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(status_code=404, detail="Candidate attempt not found")
        
    # If it's a legacy attempt tied to a session, check authorization
    if attempt.session_id:
        # We need to load session separately if not loaded
        from app.models.test_session import TestSession
        session_res = await db.execute(select(TestSession).where(TestSession.id == attempt.session_id))
        session = session_res.scalar_one_or_none()
        if session and session.created_by != current_admin.id:
            raise HTTPException(status_code=403, detail="Not authorized")
    elif attempt.admin_id and attempt.admin_id != current_admin.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    return {
        "id": str(attempt.id),
        "candidate_name": attempt.candidate_name,
        "candidate_email": attempt.candidate_email,
        "status": attempt.status,
        "score": attempt.score,
        "started_at": attempt.started_at,
        "submitted_at": attempt.submitted_at,
        "time_taken_seconds": attempt.time_taken_seconds,
        "problems": [
            {
                "problem_id": cp.problem_id,
                "title": cp.problem.title,
                "difficulty": cp.problem.difficulty,
                "status": cp.status,
                "language": cp.language,
                "score": cp.score,
                "passed_cases": cp.passed_cases,
                "total_cases": cp.total_cases,
                "submitted_code": cp.submitted_code,
                "test_results": cp.test_results
            } for cp in attempt.problems
        ]
    }
