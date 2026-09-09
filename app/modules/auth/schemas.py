import uuid

from typing import List
from pydantic import Field
from datetime import datetime

from app.shared.schemas import IBaseModel, BaseResponse
from app.modules.books_example.schemas import Book


class UserModel(IBaseModel):
    uid: uuid.UUID = Field(..., description="用户ID")
    username: str = Field(..., description="用户名", max_length=16)
    email: str = Field(..., description="邮箱", max_length=40)
    first_name: str = Field(..., description="名", max_length=30)
    last_name: str = Field(..., description="姓", max_length=30)
    is_verified: bool = Field(..., description="是否验证")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    books: List[Book] = Field([], description="用户图书列表")

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
    data: UserModel = Field(..., description="用户信息")

class LoginUserData(IBaseModel):
    email: str = Field(..., description="邮箱", max_length=40)
    user_uid: str = Field(..., description="用户ID")
    role: str = Field(..., description="角色")

class LoginDataModel(IBaseModel):
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    user: LoginUserData = Field(..., description="用户信息")

class LoginResponse(BaseResponse):
    data: LoginDataModel = Field(..., description="用户信息")
