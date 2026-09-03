from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import http_utils
from app.shared.routes import create_router
from app.utils.decorators import exception_handler
from app.db import get_session

from .schemas import UserCreateModel, UserResponse
from .service import UserService


router = create_router("auth")
user_service = UserService()

@router.post("/signup", summary="用户注册", response_model=UserResponse)
@exception_handler("用户注册")
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        return http_utils.get_response(code=400, message="邮箱已被注册", data=None)
    else:
        new_user = await user_service.create_user(user_data, session)
        return http_utils.get_response(code=200, message="注册成功", data=new_user)
