from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Credentials(Base):
    __tablename__ = "credentials"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    domain: Mapped[str] = mapped_column(String(100))
    auth_token: Mapped[str] = mapped_column(String(100))
    refresh_token: Mapped[str] = mapped_column(String(100))
    client_id: Mapped[str] = mapped_column(String(100), nullable=True)
    client_secret: Mapped[str] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"Credentials(id={self.id}, domain={self.domain}, client_id={self.client_id})"

# AUTH_ID=db7c6c829332d
# AUTH_EXPIRES=3600
# REFRESH_ID=3beb20d8
# member_id=46d64cf1
# status=L
# PLACEMENT=DEFAULT
# PLACEMENT_OPTIONS=%7B%22any%22%3A%22119%5C%2F%22%7D'

# alembic revision --autogenerate -m "initial"
# alembic revision --autogenerate -m "Add fields to entity model"
# alembic upgrade head
