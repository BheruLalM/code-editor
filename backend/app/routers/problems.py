from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.problem import Problem

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("/")
async def get_problems(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Problem))
    problems = result.scalars().all()
    return [{
        "id": p.id,
        "title": p.title,
        "difficulty": p.difficulty,
        "tags": p.tags,
        "time_limit_seconds": p.time_limit_seconds
    } for p in problems]

@router.get("/{problem_id}")
async def get_problem(problem_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    p = result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")
        
    return {
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
