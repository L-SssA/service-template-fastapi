from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.utils.auth import generate_password_hash

from .schemas import UserCreateModel
from .models import User

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def user_exists(self, email, session: AsyncSession):
        existing_user = await self.get_user_by_email(email, session)
        return existing_user is not None

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(
            user_data_dict["password"])

        session.add(new_user)
        await session.commit()

        return new_user
