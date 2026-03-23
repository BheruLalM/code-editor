import time
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.database import get_db
from app.models.problem import Problem
from app.services.executor import run_test_cases, check_executor_health, MAX_CODE_SIZE

router = APIRouter(prefix="/execute", tags=["execute"])

# ── Rate limiting (in-memory, 5 req/min per IP) ──────────────────────────────
_rate_store: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT = 5
RATE_WINDOW = 60  # seconds

def check_rate_limit(ip: str):
    now = time.time()
    window_start = now - RATE_WINDOW
    _rate_store[ip] = [t for t in _rate_store[ip] if t > window_start]
    if len(_rate_store[ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: max {RATE_LIMIT} requests per minute"
        )
    _rate_store[ip].append(now)


class RunRequest(BaseModel):
    problem_id: str
    language: str
    code: str


@router.post("/run")
async def execute_run(req: RunRequest, request: Request, db: AsyncSession = Depends(get_db)):
    # Rate limit
    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(client_ip)

    # Code size limit
    if len(req.code) > MAX_CODE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Code exceeds {MAX_CODE_SIZE} character limit ({len(req.code)} chars)"
        )

    result = await db.execute(select(Problem).where(Problem.id == req.problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    run_results = await run_test_cases(
        req.code,
        req.language,
        problem.visible_test_cases,
        is_hidden=False,
        time_limit=problem.time_limit_seconds
    )

    passed = sum(1 for r in run_results if r["passed"])
    total = len(run_results)
    total_time = sum(r.get("execution_time_ms", 0) for r in run_results)

    return {
        "results": run_results,
        "passed": passed,
        "total": total,
        "execution_time_ms": total_time
    }


@router.get("/health")
async def executor_health():
    return await check_executor_health()
