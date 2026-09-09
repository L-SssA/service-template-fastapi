from pydantic import Field

from app.shared.schemas import IBaseModel, BaseResponse


class UserCreateModel(IBaseModel):
    username: str = Field(..., description="用户名", max_length=16)
    email: str = Field(..., description="邮箱", max_length=40)
    first_name: str = Field(..., description="名", max_length=30)
    last_name: str = Field(..., description="姓", max_length=30)
    password: str = Field(..., description="密码", min_length=6)

class UserLoginModel(IBaseModel):
    email: str = Field(..., description="邮箱", max_length=40)
    password: str = Field(..., description="密码", min_length=6)

class UserResponse(BaseResponse):
    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "data": {
                    "uid": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "test",
                    "email": "test@example.com",
                    "first_name": "",
                    "last_name": "",
                    "is_verified": True,
                    "created_at": "2023-01-01T12:00:00",
                    "updated_at": "2023-01-01T12:00:00",

                },
                "message": "注册成功",
            },
        }
