import uuid

from datetime import datetime

from app.shared.schemas import IBaseModel, BaseResponse


class Book(IBaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

class BookCreateModel(IBaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdateModel(IBaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

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
