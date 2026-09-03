from passlib.context import CryptContext

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
