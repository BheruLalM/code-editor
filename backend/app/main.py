from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# Import ALL models at very top
from app.models import Base, Admin, Problem, TestSession, CandidateAttempt
from app.database import AsyncSessionLocal, get_db
from app.config import settings

from app.routers.admin_sessions import router as admin_sessions_router
from app.routers.admin_candidates import router as admin_candidates_router
from app.routers.problems import router as problems_router
from app.routers.execute import router as execute_router
from app.routers.test_link import router as test_link_router

from app.data.seed_admin import seed_default_admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("CodeArena starting up...")

    # Seed problems and default admin
    async with AsyncSessionLocal() as db:
        from app.data.problems import seed_problems
        await seed_problems(db)
        await seed_default_admin(db)

    # Check Judge0 availability (best-effort)
    from app.services.executor import check_executor_health
    exec_status = await check_executor_health()
    print(f"Executor status: {exec_status['status']}")

    yield
    print("CodeArena shutting down...")

app = FastAPI(
    title="CodeArena API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
origins = settings.ALLOWED_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include ALL routers
app.include_router(admin_sessions_router)
app.include_router(admin_candidates_router)
app.include_router(problems_router)
app.include_router(execute_router)
app.include_router(test_link_router)

@app.get("/")
async def root():
    return {"name": "CodeArena API", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    from app.services.executor import check_executor_health
    executor = await check_executor_health()

    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "database": db_status,
        "executor": "judge0",
        "executor_status": executor
    }
