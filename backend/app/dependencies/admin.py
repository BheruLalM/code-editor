from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.database import get_db
from app.models.admin import Admin
from app.services.auth_service import decode_admin_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/auth/login")

async def get_current_admin(
  token: str = Depends(oauth2_scheme),
  db: AsyncSession = Depends(get_db)
) -> Admin:
  payload = decode_admin_token(token)
  
  # For async SQLAlchemy:
  admin = await db.get(Admin, UUID(payload["sub"]))
  
  if not admin or not admin.is_active:
    raise HTTPException(status_code=401, detail="Invalid admin credentials")
  return admin
