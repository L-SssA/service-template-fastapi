from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.auth.service import UserService
from app.modules.books_example.service import BookService

from .models import Review
from .schemas import ReviewCreateModel

book_service = BookService()
user_service = UserService()

class ReviewService:

    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession
    ):
        book = await book_service.get_book(book_uid, session)
        user = await user_service.get_user_by_email(user_email, session)

        review_data_dict = review_data.model_dump()
        new_review = Review(**review_data_dict)
        new_review.user = user
        new_review.book = book

        session.add(new_review)
        await session.commit()

        return new_review

    async def get_review(self, review_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def delete_review(self, review_uid: str, session: AsyncSession):
        review_to_delete = await self.get_review(review_uid, session)
        if not review_to_delete:
            return None
        else:
            await session.delete(review_to_delete)
            await session.commit()
            return review_to_delete
