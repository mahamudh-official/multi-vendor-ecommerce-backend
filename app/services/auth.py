from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import UserRegister
from app.schemas.user import UserUpdate


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register(self, data: UserRegister)-> User:
        existing_email = self.user_repository.get_by_email(data.email)
        if existing_email:
            raise ValueError("Email already exists")

        existing_username = self.user_repository.get_by_username(data.username)
        if existing_username:
            raise ValueError("Username already exists")

        password_hash = hash_password(data.password)

        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            username=data.username,
            email=data.email,
            password_hash=password_hash,
            phone_number=data.phone_number,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, email: str, password: str):
        user = self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("User not found")
        if not user.is_active:
            raise ValueError("User is not active")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid password")

        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}

    def update(self, user: User, update_data: UserUpdate) -> User:

        update_dict = update_data.model_dump(exclude_unset=True)
        return self.user_repository.update(user, update_dict)
        
        