

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base


class BitrixSettings(Base):
    __tablename__ = "bitrix_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    domain: Mapped[str] = mapped_column(String(100))
    auth_token: Mapped[str] = mapped_column(String(100))
    refresh_token: Mapped[str] = mapped_column(String(100))
    client_id: Mapped[str] = mapped_column(String(100))
    client_secret: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"BitrixSettings(id={self.id}, domain={self.domain}, client_id={self.client_id})"
