import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from leadsy_api.database.base import Base


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    email: Mapped[str] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(60))
    expires_at: Mapped[datetime.datetime] = mapped_column()
