import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings
from app.data.problems import seed_problems

async def main():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as db:
        await seed_problems(db)
        print("Successfully updated all problems with new starter code.")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
