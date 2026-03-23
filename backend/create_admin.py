import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from app.config import settings
from app.models.admin import Admin
from app.services.auth_service import get_password_hash
from app.data.problems import seed_problems

async def main():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as db:
        await seed_problems(db)
        
        result = await db.execute(select(Admin).where(Admin.username == "admin"))
        existing = result.scalar_one_or_none()
        
        if existing:
            print("Admin already exists!")
        else:
            admin = Admin(
                username="admin",
                email="admin@codearena.com",
                hashed_password=get_password_hash("admin123"),
                full_name="CodeArena Admin",
                is_active=True
            )
            db.add(admin)
            await db.commit()
            print("Successfully created admin account: admin / admin123")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
