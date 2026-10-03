
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def update(self, user: User, update_data: UserUpdate) -> User:

        if update_data.phone_number is not None:
            existing_user = self.user_repository.get_by_phone_number(update_data.phone_number)
            if existing_user and existing_user.id != user.id:
                raise ValueError("Phone number already exists")


        update_dict = update_data.model_dump(exclude_unset=True)
        return self.user_repository.update(user, update_dict)
        
        