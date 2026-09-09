import uuid

from typing import List
from pydantic import Field
from datetime import datetime

from app.shared.schemas import IBaseModel, BaseResponse

class Book(IBaseModel):
    uid: uuid.UUID = Field(..., description="书籍ID")
    title: str = Field(..., description="标题")
    author: str = Field(..., description="作者")
    publisher: str = Field(..., description="出版社")
    published_date: datetime = Field(..., description="出版日期")
    page_count: int = Field(..., description="页数")
    language: str = Field(..., description="语言")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class BookCreateModel(IBaseModel):
    title: str = Field(..., description="标题", min_length=1, max_length=255)
    author: str = Field(..., description="作者", min_length=1, max_length=255)
    publisher: str = Field(
        ..., description="出版社", min_length=1, max_length=255)
    published_date: str = Field(
        ..., description="出版日期", min_length=1, max_length=255)
    page_count: int = Field(..., description="页数", gt=0)
    language: str = Field(..., description="语言", min_length=1, max_length=255)

class BookUpdateModel(IBaseModel):
    title: str = Field(..., description="标题", min_length=1, max_length=255)
    author: str = Field(..., description="作者", min_length=1, max_length=255)
    publisher: str = Field(
        ..., description="出版社", min_length=1, max_length=255)
    page_count: int = Field(..., description="页数", gt=0)
    language: str = Field(
        ..., description="语言", min_length=1, max_length=255)

class AllBooksResponse(BaseResponse):
    data: List[Book] = Field(..., description="书籍列表")

class BookResponse(BaseResponse):
    data: Book = Field(..., description="书籍")
