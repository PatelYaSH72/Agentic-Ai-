from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user_data: UserCreate) -> User:

        existing_user = self.user_repository.get_by_email(
            user_data.email
        )

        if existing_user:
            from app.core.exceptions import EmailAlreadyExistsException

        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )

        return self.user_repository.create(new_user)