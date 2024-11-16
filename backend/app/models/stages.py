


from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from ..db.db import Base


class Stages(Base):
    __tablename__ = "stages"

    id: Mapped[int] = mapped_column(primary_key=True)
    entity_id: Mapped[str | None] = mapped_column(String(50))
    category_id: Mapped[int]
    status_id: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(100))
    semantic: Mapped[str] = mapped_column(String(5))

    def __repr__(self) -> str:
        return f"Stages(id={self.id}, entity_id={self.entity_id}, category_id={self.category_id}, status_id={self.status_id}, name={self.name}, semantic={self.semantic})"

