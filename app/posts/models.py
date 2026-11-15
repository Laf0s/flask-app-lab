from datetime import datetime, timezone
from sqlalchemy import Integer, String, Text, DateTime, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app import db

POST_CATEGORIES = ("news", "publication", "tech", "other")


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    category: Mapped[str] = mapped_column(
        Enum(*POST_CATEGORIES, name="post_category_enum"),
        nullable=False,
        default="other"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    author: Mapped[str] = mapped_column(String(20), default="Anonymous", nullable=False)

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title!r}, category={self.category!r})>"