import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.admin import Admin

async def seed_default_admin(db: AsyncSession):
    # Check if any admin exists
    result = await db.execute(select(Admin))
    admin = result.scalars().first()
    
    if not admin:
        print("Seeding default admin...")
        admin = Admin(
            id=uuid.uuid4(),
            username="admin",
            email="admin@codearena.com",
            hashed_password="not-used-anymore",
            full_name="Default Administrator",
            is_active=True
        )
        db.add(admin)
        await db.commit()
    else:
        print(f"Admin already exists: {admin.username}")
