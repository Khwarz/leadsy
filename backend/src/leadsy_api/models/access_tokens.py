from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from leadsy_api.database.base import Base
from leadsy_api.models.users import User


class PersonalAccessToken(Base):
    __tablename__ = "personal_access_tokens"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id", ondelete="CASCADE", onupdate="CASCADE", name="user_token_fk"
        )
    )
    token: Mapped[str] = mapped_column(unique=True)

    user: Mapped[User] = relationship()

    expires_at: Mapped[datetime | None] = mapped_column(nullable=True)

    created_at: Mapped[datetime | None] = mapped_column(
        server_default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=True
    )
