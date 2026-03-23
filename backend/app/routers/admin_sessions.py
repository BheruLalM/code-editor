import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.admin import Admin
from app.models.test_session import TestSession, DifficultyFilter
from app.models.candidate_attempt import CandidateAttempt
from app.dependencies.admin import get_current_admin
from app.config import settings

router = APIRouter(prefix="/admin/sessions", tags=["admin-sessions"])

def _difficulty_filter_to_str(val):
    # DifficultyFilter is a str-enum, but normalize defensively for JSON serialization.
    return getattr(val, "value", val)

class CreateSessionRequest(BaseModel):
    title: str
    description: Optional[str] = None
    difficulty_filter: DifficultyFilter = DifficultyFilter.any
    time_limit_minutes: int = 45
    max_attempts: Optional[int] = None
    expires_at: Optional[datetime] = None

class UpdateSessionRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit_minutes: Optional[int] = None
    is_active: Optional[bool] = None

@router.post("/")
async def create_session(
    data: CreateSessionRequest, 
    db: AsyncSession = Depends(get_db), 
    current_admin: Admin = Depends(get_current_admin)
):
    session_token = secrets.token_hex(16)
    new_session = TestSession(
        session_token=session_token,
        title=data.title,
        description=data.description,
        difficulty_filter=data.difficulty_filter,
        time_limit_minutes=data.time_limit_minutes,
        max_attempts=data.max_attempts,
        expires_at=data.expires_at,
        created_by=current_admin.id
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    shareable_link = f"{settings.FRONTEND_URL}/test/{session_token}"
    return {
        "session": {
            "id": str(new_session.id),
            "session_token": new_session.session_token,
            "title": new_session.title,
            "description": new_session.description,
            "difficulty_filter": _difficulty_filter_to_str(new_session.difficulty_filter),
            "time_limit_minutes": new_session.time_limit_minutes,
            "is_active": new_session.is_active,
            "max_attempts": new_session.max_attempts,
            "expires_at": new_session.expires_at,
            "created_at": new_session.created_at,
            "created_by": str(new_session.created_by),
        },
        "shareable_link": shareable_link
    }

@router.get("/")
async def get_sessions(
    db: AsyncSession = Depends(get_db), 
    current_admin: Admin = Depends(get_current_admin)
):
    result = await db.execute(
        select(TestSession)
        .where(TestSession.created_by == current_admin.id)
        .order_by(desc(TestSession.created_at))
    )
    sessions = result.scalars().all()
    
    resp = []
    for s in sessions:
        attempts_res = await db.execute(select(CandidateAttempt).where(CandidateAttempt.session_id == s.id))
        attempts = attempts_res.scalars().all()
        
        submitted = [a for a in attempts if a.status == "submitted"]
        scores = [a.score for a in submitted if a.score is not None]
        avg_score = sum(scores) / len(scores) if scores else None
        
        resp.append({
            "id": str(s.id),
            "session_token": s.session_token,
            "title": s.title,
            "difficulty_filter": _difficulty_filter_to_str(s.difficulty_filter),
            "time_limit_minutes": s.time_limit_minutes,
            "is_active": s.is_active,
            "created_at": s.created_at,
            "expires_at": s.expires_at,
            "candidate_count": len(attempts),
            "submitted_count": len(submitted),
            "avg_score": avg_score
        })
    return resp

@router.get("/{session_id}")
async def get_session_detail(
    session_id: str,
    db: AsyncSession = Depends(get_db), 
    current_admin: Admin = Depends(get_current_admin)
):
    result = await db.execute(
        select(TestSession).where(
            TestSession.id == session_id,
            TestSession.created_by == current_admin.id
        )
    )
    s = result.scalar_one_or_none()
    if not s:
        raise HTTPException(404, "Session not found")
        
    attempts_res = await db.execute(select(CandidateAttempt).where(CandidateAttempt.session_id == s.id))
    attempts = attempts_res.scalars().all()
    submitted = [a for a in attempts if a.status == "submitted"]
    scores = [a.score for a in submitted if a.score is not None]
    
    return {
        "id": str(s.id),
        "session_token": s.session_token,
        "title": s.title,
        "description": s.description,
        "difficulty_filter": _difficulty_filter_to_str(s.difficulty_filter),
        "time_limit_minutes": s.time_limit_minutes,
        "is_active": s.is_active,
        "created_at": s.created_at,
        "expires_at": s.expires_at,
        "max_attempts": s.max_attempts,
        "shareable_link": f"{settings.FRONTEND_URL}/test/{s.session_token}",
        "candidate_count": len(attempts),
        "submitted_count": len(submitted),
        "avg_score": sum(scores) / len(scores) if scores else None,
        "best_score": max(scores) if scores else None
    }

@router.patch("/{session_id}")
async def update_session(
    session_id: str,
    data: UpdateSessionRequest,
    db: AsyncSession = Depends(get_db), 
    current_admin: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(TestSession).where(TestSession.id == session_id, TestSession.created_by == current_admin.id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(404, "Session not found")
        
    if data.title is not None: session.title = data.title
    if data.description is not None: session.description = data.description
    if data.time_limit_minutes is not None: session.time_limit_minutes = data.time_limit_minutes
    if data.is_active is not None: session.is_active = data.is_active
    
    await db.commit()
    await db.refresh(session)
    return {
        "id": str(session.id),
        "session_token": session.session_token,
        "title": session.title,
        "description": session.description,
        "difficulty_filter": _difficulty_filter_to_str(session.difficulty_filter),
        "time_limit_minutes": session.time_limit_minutes,
        "is_active": session.is_active,
        "max_attempts": session.max_attempts,
        "expires_at": session.expires_at,
        "created_at": session.created_at,
        "created_by": str(session.created_by),
    }

@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    db: AsyncSession = Depends(get_db), 
    current_admin: Admin = Depends(get_current_admin)
):
    result = await db.execute(select(TestSession).where(TestSession.id == session_id, TestSession.created_by == current_admin.id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(404, "Session not found")
        
    session.is_active = False
    await db.commit()
    return {"message": "Session deactivated"}
