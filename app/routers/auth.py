from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import LoginRequest, APIResponse, LoginData, UserResponse
from app.auth import authenticate_admin, create_access_token
from app.config import settings

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/login", response_model=APIResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Admin login endpoint
    """
    admin = authenticate_admin(db, login_data.username, login_data.password)
    
    if not admin:
        return APIResponse(
            success=False,
            message="Invalid username or password",
            data=None
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    
    return APIResponse(
        success=True,
        message="Login successful",
        data=LoginData(
            token=access_token,
            user=UserResponse(username=admin.username)
        )
    )

