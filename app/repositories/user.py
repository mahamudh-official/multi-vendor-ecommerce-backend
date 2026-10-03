from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_by_id(self, id:int)-> User | None:
        smtm = select(User).where(User.id == id)
        result = self.db.execute(smtm)
        return result.scalar_one_or_none()

    def get_by_email(self, email:str)-> User | None:
        smtm = select(User).where(User.email == email)
        result = self.db.execute(smtm)
        return result.scalar_one_or_none()

    def get_by_username(self, username:str)-> User | None:
        smtm = select(User).where(User.username == username)
        result = self.db.execute(smtm)
        return result.scalar_one_or_none()

    def get_by_phone_number(self, phone_number:str)-> User | None:
        smtm = select(User).where(User.phone_number == phone_number)
        result = self.db.execute(smtm)
        return result.scalar_one_or_none()

    def update(self, user:User, update_data: dict)-> User:
        for key, value in update_data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user