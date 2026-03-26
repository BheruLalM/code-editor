from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.database import get_db
from app.models.admin import Admin
from app.services.auth_service import decode_admin_token

from sqlalchemy import select

async def get_current_admin(
  db: AsyncSession = Depends(get_db)
) -> Admin:
  # Simply fetch the first admin (the seeded default one)
  result = await db.execute(select(Admin))
  admin = result.scalars().first()
  
  if not admin:
    raise HTTPException(status_code=500, detail="Default admin not seeded")
  return admin
