import uuid

from datetime import datetime
from pydantic import Field
from typing import Optional
from app.shared.schemas import IBaseModel, BaseResponse

class ReviewModel(IBaseModel):
    uid: uuid.UUID = Field(..., description="评论ID")
    rating: int = Field(..., description="评分")
    review_text: str = Field(..., description="评论内容")
    user_uid: Optional[uuid.UUID] = Field(..., description="用户ID")
    book_uid: Optional[uuid.UUID] = Field(..., description="书籍ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class ReviewCreateModel(IBaseModel):
    rating: int = Field(..., description="评分")
    review_text: str = Field(..., description="评论内容")


class ReviewCreateResponse(BaseResponse):
    data: Optional[ReviewModel] = Field(..., description="评论信息")
