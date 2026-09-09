from datetime import timedelta, datetime
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import http_utils
from app.shared.routes import create_router
from app.utils.decorators import exception_handler
from app.db import get_session
from app.utils.auth import verify_password, create_token_pairs
from app.db.redis import add_jti_to_blocklist

from .schemas import UserCreateModel, UserLoginModel, UserResponse
from .service import UserService
from .dependencies import AccessTokenBearer, RefreshTokenBearer


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


@router.post("/login", summary="用户登录")
@exception_handler("用户登录")
async def login_user(
    login_data: UserLoginModel,
    session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            user_data = {
                "email": user.email,
                "user_uid": str(user.uid),
            }
            access_token, refresh_token = create_token_pairs(user_data)

            return http_utils.get_response(
                code=200,
                message="登录成功",
                data={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user_data
                }
            )

    return http_utils.get_response(code=400, message="邮箱或密码错误", data=None)


@router.get("/refresh_token", summary="刷新token")
@exception_handler("刷新token")
async def get_new_access_token(
    token_details: dict = Depends(RefreshTokenBearer()),
):
    expiry_timestamp = token_details.get("exp", datetime.now())

    user_data = token_details.get("user", None)

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now() and user_data:

        access_token, refresh_token = create_token_pairs(user_data)

        return http_utils.get_response(
            code=200,
            message="刷新成功",
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_data
            }
        )

    return http_utils.get_response(code=400, message="refresh_token已过期或无效", data=None)


@router.get("/logout", summary="退出登录")
@exception_handler("退出登录")
async def revoke_token(
    token_details: dict = Depends(AccessTokenBearer()),
):
    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return http_utils.get_response(code=200, message="退出登录成功", data=None)
