import jwt
import uuid

from loguru import logger
from datetime import timedelta, datetime
from passlib.context import CryptContext

import app.config as config

password_context = CryptContext(schemes=["bcrypt"])


def generate_password_hash(password: str) -> str:
    """
    生成密码哈希值

    :param password: 明文密码
    :return: 哈希值
    """
    return password_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    """
    校验密码

    :param password: 明文密码
    :param hash: 哈希值
    :return: 是否匹配
    """
    return password_context.verify(password, hash)


def create_access_token(
    user_data: dict,
    expiry: timedelta = timedelta(seconds=config.jwt_expiry_seconds),
    refresh: bool = False
):
    """
    生成JWT令牌

    :param user_data: 用户数据
    :param expiry: 过期时间
    :return: JWT令牌
    """
    payload = {}

    # 用户数据
    payload["user"] = user_data
    # 过期时间
    payload["exp"] = datetime.now() + expiry
    # uuid
    payload["jti"] = str(uuid.uuid4())
    # 是否刷新
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload,
        key=config.jwt_secret_key,
        algorithm=config.jwt_algorithm,
    )

    return token

def create_token_pairs(user_data: dict):
    """
    生成JWT令牌对

    :param user_data: 用户数据
    :return: 访问令牌和刷新令牌
    """
    access_token = create_access_token(user_data)
    refresh_token = create_access_token(
        user_data, timedelta(seconds=config.jwt_refresh_expiry_seconds), refresh=True)

    return access_token, refresh_token

def decode_token(token: str) -> dict:
    """
    解码JWT令牌

    :param token: JWT令牌
    :return: 用户数据
    """
    try:
        return jwt.decode(
            jwt=token,
            key=config.jwt_secret_key,
            algorithms=[config.jwt_algorithm],
        )
    except jwt.PyJWTError as e:
        logger.error(e)
        return None
