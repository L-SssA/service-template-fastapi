from typing import Any

def get_response(code: int, data: Any = None, message: str = "操作成功"):
    return {
        'code': code,
        'data': data,
        'message': message
    }
