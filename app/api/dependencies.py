from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User, UserRole
from app.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:

    user_repository = UserRepository(db)
    

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (KeyError,TypeError, ValueError) as exc:
        raise HTTPException(status_code=401,
            detail= str(exc), headers={"WWW-Authenticate": "Bearer"})

    user = user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401,
            detail= "User not found", headers={"WWW-Authenticate": "Bearer"})

    return user


def required_role(*allowed_roles: UserRole):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return current_user

    return role_checker
