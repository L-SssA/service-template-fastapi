from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from loguru import logger

from app.utils import http_utils
from app.db import get_session
from app.shared.routes import create_router
from app.utils.decorators import exception_handler
from app.modules.auth.dependencies import get_current_user_from_token
from app.modules.auth.models import User

from .schemas import ReviewCreateModel, ReviewResponse
from .service import ReviewService

router = create_router("reviews")
review_service = ReviewService()

@router.post("/book/{book_uid}", summary="添加给书籍评论", response_model=ReviewResponse)
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


@router.get("/{review_uid}", summary="获取评论详情", response_model=ReviewResponse)
@exception_handler("获取评论详情")
async def get_review(
    review_uid: str,
    session: AsyncSession = Depends(get_session)
):
    review = await review_service.get_review(review_uid=review_uid, session=session)
    if review:
        return http_utils.get_response(code=200, data=review, message="操作成功")
    else:
        logger.warning(f"获取评论详情失败，review_uid: {review_uid}")
        return http_utils.get_response(code=404, message="评论不存在")

@router.delete("/{review_uid}", summary="删除评论", response_model=ReviewResponse)
@exception_handler("删除评论")
async def delete_review(
    review_uid: str,
    session: AsyncSession = Depends(get_session)
):
    review = await review_service.delete_review(review_uid=review_uid, session=session)
    if review:
        return http_utils.get_response(code=300, data=review, message="评论删除成功")
    else:
        logger.warning(f"删除评论失败，book_uid: {review_uid}")
        return http_utils.get_response(code=404, message="评论不存在")
