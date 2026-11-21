from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Text, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

if TYPE_CHECKING:
    from app.users.models import User

POST_CATEGORIES = ("news", "publication", "tech", "other")

post_tags = db.Table(
    "post_tags",
    db.Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


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

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")

    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title!r}, category={self.category!r})>"

class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name={self.name!r})>"