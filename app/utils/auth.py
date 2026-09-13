import jwt
import uuid
import bcrypt

from loguru import logger
from datetime import timedelta, datetime
from itsdangerous import URLSafeTimedSerializer

import app.config as config


serializer = URLSafeTimedSerializer(
    secret_key=config.jwt_secret_key,
    salt="email-configuration"
)


def generate_password_hash(password: str) -> str:
    """
    生成密码哈希值

    :param password: 明文密码
    :return: 哈希值
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hash: str) -> bool:
    """
    校验密码

    :param password: 明文密码
    :param hash: 哈希值
    :return: 是否匹配
    """
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))


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


def create_url_safe_token(data: dict):
    return serializer.dumps(data)


def decode_url_safe_token(token: str):
    try:
        return serializer.loads(token)
    except Exception as e:
        logger.error(e)
        return None
