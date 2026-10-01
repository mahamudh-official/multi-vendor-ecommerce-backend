from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db))-> User:


    user_repository = UserRepository(db)
    payload = decode_access_token(token)

    try:
        user_id = int(payload['sub'])
    except KeyError:
        raise ValueError("Invalid token payload: 'sub' field is missing")

    user = user_repository.get_by_id(user_id)
    if not user:
        raise ValueError("User not found")

    return user