from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from app.utils.auth import decode_token
from app.db.redis import token_in_blocklisted

class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token_data = decode_token(creds.credentials)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token不存在或已过期",
            )

        if await token_in_blocklisted(token_data.get("jti", None)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token不存在或已过期，请重新登陆。"
            )

        self.verify_token_data(token_data)

        return token_data

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("请在子类中实现verify_token_data方法")

class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get("refresh", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="请使用Access_Token访问",
            )


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="请使用Refresh_Token访问",
            )
