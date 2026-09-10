import uuid

from typing import List, Optional
from pydantic import Field
from datetime import datetime

from app.shared.schemas import IBaseModel, BaseResponse
from app.modules.reviews_example.schemas import ReviewModel

class BookModel(IBaseModel):
    uid: uuid.UUID = Field(..., description="书籍ID")
    title: str = Field(..., description="标题")
    author: str = Field(..., description="作者")
    publisher: str = Field(..., description="出版社")
    published_date: datetime = Field(..., description="出版日期")
    page_count: int = Field(..., description="页数")
    language: str = Field(..., description="语言")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class BookDetailModel(BookModel):
    reviews: List[ReviewModel] = Field(..., description="评论列表")

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
    data: Optional[List[BookModel]] = Field(..., description="书籍列表")

class BookResponse(BaseResponse):
    data: Optional[BookModel] = Field(..., description="书籍")


class BookDetailResponse(BaseResponse):
    data: Optional[BookDetailModel] = Field(..., description="书籍")
