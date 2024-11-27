from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..db.db import Base


class BitrixSettings(Base):
    __tablename__ = "bitrix_settings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    domain: Mapped[str] = mapped_column(String(100))
    auth_token: Mapped[str] = mapped_column(String(100))
    refresh_token: Mapped[str] = mapped_column(String(100))
    client_id: Mapped[str] = mapped_column(String(100))
    client_secret: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"BitrixSettings(id={self.id}, domain={self.domain}, client_id={self.client_id})"

# AUTH_ID=4bc046670073b32a001252ad00002e0d403807da3fd2b6cdddb6ad4935c32d7c6c2182
# AUTH_EXPIRES=3600
# REFRESH_ID=3b3f6e670073b32a001252ad00002e0d40380785cbac819c5ebcf2321fd4727a0d4248
# member_id=46daf0002614a639c844739d27cf70c1
# status=L
# PLACEMENT=DEFAULT
# PLACEMENT_OPTIONS=%7B%22any%22%3A%22119%5C%2F%22%7D'
