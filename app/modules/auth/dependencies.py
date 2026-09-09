from typing import List
from fastapi import status, Request, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.exception_schemas import HttpException
from app.utils.auth import decode_token
from app.db.redis import token_in_blocklisted
from app.db import get_session

from .service import UserService
from .models import User

user_service = UserService()

class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token_data = decode_token(creds.credentials)

        if not token_data:
            raise HttpException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Token不存在或已过期",
            )

        if await token_in_blocklisted(token_data.get("jti", None)):
            raise HttpException(
                status_code=status.HTTP_403_FORBIDDEN,
                detmessageail="Token不存在或已过期，请重新登陆。"
            )

        self.verify_token_data(token_data)

        return token_data

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("请在子类中实现verify_token_data方法")

class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get("refresh", True):
            raise HttpException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="请使用Access_Token访问",
            )


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get("refresh", False):
            raise HttpException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="请使用Refresh_Token访问",
            )


async def get_current_user_from_token(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
) -> User:
    user_email = token_details["user"]["email"]

    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user_from_token)):
        if current_user.role not in self.allowed_roles:
            raise HttpException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="您没有权限执行此操作",
            )

        return True
