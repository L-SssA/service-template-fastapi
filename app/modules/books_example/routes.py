from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.utils import http_utils
from app.utils.decorators import exception_handler
from app.shared.routes import create_router
from app.db import get_session
from app.modules.auth.dependencies import AccessTokenBearer, RoleChecker

from .schemas import (
    BookCreateModel,
    BookUpdateModel,
    AllBooksResponse,
    BookResponse,
    BookDetailResponse
)
from .service import BookService

router = create_router("books")
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", 'user'])

@router.get("/", summary="查询所有书籍", response_model=AllBooksResponse, dependencies=[Depends(access_token_bearer), Depends(role_checker)])
@exception_handler("查询所有书籍")
async def get_all_books(
    session: AsyncSession = Depends(get_session),
):
    books = await book_service.get_all_books(session)
    return http_utils.get_response(code=200, data=books, message="操作成功")


@router.get("/user/{user_uid}", summary="查询用户提交的书籍", response_model=AllBooksResponse, dependencies=[Depends(role_checker)])
@exception_handler("查询用户提交的书籍")
async def get_user_book_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.get_user_books(user_uid, session)
    return http_utils.get_response(code=200, data=books, message="操作成功")


@router.post("/", summary="创建书籍", response_model=BookResponse, dependencies=[Depends(role_checker)])
@exception_handler("创建书籍")
async def create_book(
    data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    user_id = token_details["user"]["user_uid"]
    new_book = await book_service.create_book(data, user_id, session)
    return http_utils.get_response(code=201, data=new_book, message="创建成功")


@router.get("/{book_uid}", summary="查询书籍", response_model=BookDetailResponse, dependencies=[Depends(access_token_bearer), Depends(role_checker)])
@exception_handler("查询书籍")
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
):
    book = await book_service.get_book(book_uid, session)
    if book:
        return http_utils.get_response(code=200, data=book, message="操作成功")
    else:
        logger.warning(f"查询书籍失败，book_uid: {book_uid}")
        return http_utils.get_response(code=404, data=None, message="书籍不存在")

@router.put("/{book_uid}", summary="更新书籍", response_model=BookResponse, dependencies=[Depends(access_token_bearer), Depends(role_checker)])
@exception_handler("更新书籍")
async def update_book(
    book_uid: str,
    data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    book = await book_service.update_book(book_uid, data, session)
    if book:
        return http_utils.get_response(code=200, data=book, message="操作成功")
    else:
        logger.warning(f"更新书籍失败，book_uid: {book_uid}")
        return http_utils.get_response(code=404, data=None, message="书籍不存在")


@router.delete("/{book_uid}", summary="删除书籍", response_model=BookResponse, dependencies=[Depends(access_token_bearer), Depends(role_checker)])
@exception_handler("删除书籍")
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
):
    book = await book_service.delete_book(book_uid, session)
    if book:
        return http_utils.get_response(code=200, data=book, message="操作成功")
    else:
        logger.warning(f"删除书籍失败，book_uid: {book_uid}")
        return http_utils.get_response(code=404, data=None, message="书籍不存在")
