
import uuid
import sqlalchemy.dialects.postgresql as pg

from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, Relationship

if TYPE_CHECKING:
    from app.modules.auth.models import User
    from app.modules.books_example.models import Book

class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))

    user: Optional["User"] = Relationship(
        back_populates="reviews")
    book: Optional["Book"] = Relationship(
        back_populates="reviews")

    def __repr__(self):
        return f"<Review of book {self.book_uid} by user {self.user_uid}>"
