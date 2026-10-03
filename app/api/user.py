from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import UserResponse
from app.schemas.user import UserUpdate
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["User"],
)

@router.patch("/me", response_model=UserResponse)
def update_me(user: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        return user_service.update(current_user, user)
    except ValueError as exc:
        raise HTTPException(status_code=409,
            detail= str(exc))