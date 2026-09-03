from pydantic import Field

from app.shared.schemas import IBaseModel, BaseResponse


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
    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "data": [],
                "message": "操作成功",
            },
        }

class BookResponse(BaseResponse):
    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "data": {
                    "uid": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Example Book",
                    "author": "John Doe",
                    "publisher": "Example Publisher",
                    "published_date": "2023-01-01",
                    "page_count": 300,
                    "language": "English",
                    "created_at": "2023-01-01T12:00:00",
                    "updated_at": "2023-01-01T12:00:00",
                },
                "message": "操作成功",
            },
        }
