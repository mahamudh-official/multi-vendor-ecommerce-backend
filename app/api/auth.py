from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import UserLogin, UserLoginResponse, UserRegister, UserResponse
from app.core.database import get_db
from app.services.auth import AuthService



router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):

    try:
        user_service = AuthService(db)
        return user_service.register(user)
    except ValueError as exc:
        raise HTTPException(status_code=409,
            detail= str(exc))

@router.post("/login", response_model=UserLoginResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):

    try:
        user_service = AuthService(db)
        return user_service.login(user.email, user.password)
    except ValueError as exc:
        raise HTTPException(status_code=409,
            detail= str(exc))

    