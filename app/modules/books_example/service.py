from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from datetime import datetime

from .schemas import BookCreateModel, BookUpdateModel
from .models import Book

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def create_book(self, data: BookCreateModel, session: AsyncSession):
        book_date_dict = data.model_dump()

        new_book = Book(**book_date_dict)
        new_book.published_date = datetime.strptime(
            book_date_dict['published_date'], "%Y-%m-%d").date()

        session.add(new_book)
        await session.commit()

        return new_book

    async def update_book(self, book_uid: str, data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)

        if not book_to_update:
            return None
        else:
            for key, value in data.model_dump().items():
                setattr(book_to_update, key, value)

            await session.commit()
            return book_to_update

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if not book_to_delete:
            return None
        else:
            await session.delete(book_to_delete)
            await session.commit()
            return book_to_delete
