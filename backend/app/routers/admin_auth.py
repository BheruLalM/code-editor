from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.database import get_db
from app.models.admin import Admin
from app.services.auth_service import verify_password, create_admin_token
from app.dependencies.admin import get_current_admin

router = APIRouter(prefix="/admin/auth", tags=["admin-auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Admin).where(Admin.username == credentials.username))
    admin = result.scalar_one_or_none()
    
    if not admin or not verify_password(credentials.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_admin_token(str(admin.id), admin.username)
    return {
        "access_token": token,
        "token_type": "bearer",
        "admin": {
            "id": str(admin.id),
            "username": admin.username,
            "full_name": admin.full_name,
            "email": admin.email
        }
    }

@router.get("/me")
async def get_me(current_admin: Admin = Depends(get_current_admin)):
    return {
        "id": str(current_admin.id),
        "username": current_admin.username,
        "full_name": current_admin.full_name,
        "email": current_admin.email
    }
