from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from datetime import datetime

from app.utils.auth import generate_password_hash, verify_password

from .schemas import UserCreateModel
from .models import User

class UserService:
    async def get_user(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def user_exists(self, email, session: AsyncSession):
        existing_user = await self.get_user(email, session)
        return existing_user is not None

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(
            user_data_dict["password"])

        session.add(new_user)
        await session.commit()

        return new_user
