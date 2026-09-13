from datetime import datetime
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.schemas import BaseResponse
from app.utils import http_utils
from app.shared.routes import create_router
from app.utils.decorators import exception_handler
from app.db import get_session
from app.utils.auth import (
    verify_password,
    create_token_pairs,
    create_url_safe_token,
    decode_url_safe_token,
    generate_password_hash
)
from app.db.redis import add_jti_to_blocklist
from app import config
from app.utils.celery_client import celery_client

from .schemas import PasswordResetConfirmModel, PasswordResetRequestModel, UserCreateModel, UserLoginModel, UserResponse, UserBooksResponse, LoginResponse
from .service import UserService
from .dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    get_current_user_from_token,
    RoleChecker
)


router = create_router("auth")
user_service = UserService()
role_checker = RoleChecker(["admin", 'user'])


@router.post("/signup", summary="用户注册", response_model=UserResponse)
@exception_handler("用户注册")
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        return http_utils.get_response(code=400, message="邮箱已被注册", data=None)

    # 创建用户
    new_user = await user_service.create_user(user_data, session)

    # 发送验证邮件
    verify_token = create_url_safe_token({"email": email}, scope="signup")
    link = f"http://{config.print_host}:{config.listen_port}/auth/verify/{verify_token}"
    html_message = f"""
    <h1>验证邮箱</h1>
    <p>请点击以下链接验证您的邮箱：</p>
    <a href="{link}">验证邮箱</a>
    """

    celery_client.send_task(
        "celery_app.tasks.message.send_message",
        kwargs={
            "recipients": [email],
            "subject": "验证您的邮箱",
            "body": html_message
        }
    )

    return http_utils.get_response(code=200, message="注册成功，请查看您的邮箱并验证您的账户", data=new_user)

@router.get("/verify/{verify_token}", summary="验证邮箱")
@exception_handler("验证邮箱")
async def verify_email(verify_token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(verify_token, scope="signup")
    user_email = token_data.get("email", None)
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            return http_utils.get_response(code=404, message="用户不存在")
        await user_service.update_user(user, {"is_verified": True}, session)

        return http_utils.get_response(code=200, message="邮箱验证成功")

    return http_utils.get_response(code=400, message="验证令牌无效或已过期")


@router.post("/login", summary="用户登录", response_model=LoginResponse)
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
                "role": user.role
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


@router.get("/refresh_token", summary="刷新token", response_model=LoginResponse)
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

@router.get("/me", summary="获取当前用户信息", response_model=UserBooksResponse)
@exception_handler("获取当前用户信息")
async def get_current_user(
    user=Depends(get_current_user_from_token),
    _: bool = Depends(role_checker)
):
    return http_utils.get_response(code=200, message="获取成功", data=user)


@router.get("/logout", summary="退出登录", response_model=BaseResponse)
@exception_handler("退出登录")
async def revoke_token(
    token_details: dict = Depends(AccessTokenBearer()),
):
    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return http_utils.get_response(code=200, message="退出登录成功", data=None)


@router.post("/password-reset-request", summary="密码重置请求")
@exception_handler("密码重置请求")
async def password_reset_request(
    email_data: PasswordResetRequestModel,
):
    email = email_data.email
    verify_token = create_url_safe_token(
        {"email": email}, scope="reset_password")
    link = f"http://{config.print_host}:{config.listen_port}/auth/password-reset-confirm/{verify_token}"
    html_message = f"""
        <h1>重置您的密码</h1>
        <p>请点击以下链接重置您的密码：</p>
        <a href="{link}">重置密码</a>
        """

    celery_client.send_task(
        "celery_app.tasks.message.send_message",
        kwargs={
            "recipients": [email],
            "subject": "重置您的密码",
            "body": html_message
        }
    )

    return http_utils.get_response(code=200, message="密码重置链接已发送到您的邮箱")

@router.post("/password-reset-confirm/{verify_token}", summary="重置密码确认")
@exception_handler("重置密码确认")
async def reset_password(verify_token: str, password: PasswordResetConfirmModel, session: AsyncSession = Depends(get_session)):
    new_password = password.new_password
    confirm_new_password = password.confirm_new_password
    if new_password != confirm_new_password:
        return http_utils.get_response(code=400, message="两次输入的密码不一致")

    token_data = decode_url_safe_token(verify_token, scope="reset_password")
    user_email = token_data.get("email", None)
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            return http_utils.get_response(code=404, message="用户不存在")

        password_hash = generate_password_hash(new_password)
        await user_service.update_user(user, {"password_hash": password_hash}, session)

        return http_utils.get_response(code=200, message="密码重置成功")

    return http_utils.get_response(code=400, message="验证令牌无效或已过期")
