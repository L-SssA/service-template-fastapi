from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.utils import http_utils
from app.db import get_session
from app.shared.routes import create_router
from app.utils.decorators import exception_handler
from app.modules.auth.dependencies import get_current_user_from_token
from app.modules.auth.models import User

from .schemas import ReviewCreateModel, ReviewCreateResponse
from .service import ReviewService

router = create_router("reviews")
review_service = ReviewService()

@router.post("/book/{book_uid}", summary="添加给书籍评论", response_model=ReviewCreateResponse)
@exception_handler("添加评论")
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_session)
):
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        book_uid=book_uid,
        review_data=review_data,
        session=session
    )

    return http_utils.get_response(
        code=200,
        data=new_review,
        message="评论添加成功",
    )
