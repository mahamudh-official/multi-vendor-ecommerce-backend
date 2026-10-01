from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_by_email(self, email:str)-> User | None:
        smtm = select(User).where(User.email == email)
        result = self.db.execute(smtm)
        return result.scalar_one_or_none()

    def get_by_username(self, username:str)-> User | None:
        smtm = select(User).where(User.username == username)
        result = self.db.execute(smtm)
        return result.scalar_one_or_none()