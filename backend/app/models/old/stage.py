from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from ..db.db import Base
# from .stage_history import StageHistory


class Stages(Base):
    ''' Стадии смартпроцесса - Цех
    '''
    __tablename__ = "stages"

    id: Mapped[int] = mapped_column(primary_key=True)
    entity_id: Mapped[Optional[str]] = mapped_column(String(50))                        # кодовый идентификатор сущности и стадии (DYNAMIC_166_STAGE_31 и т.д.)
    status_id: Mapped[str] = mapped_column(String(50), index=True)                      # кодовый идентификатор стадии (DT166_31:NEW и т.д.)
    category_id: Mapped[Optional[int]]                                                  # числовой идентификатор стадии
    name: Mapped[str] = mapped_column(String(100))                                      # название стадии
    name_init: Mapped[Optional[str]] = mapped_column(String(100), server_default="")    # обобщенное название группы стадий 
    semantic: Mapped[Optional[str]] = mapped_column(String(5))                          # семантичекий код стадии

    # stage_history = relationship("StageHistory", back_populates="entity")
    stage_history = relationship("StageHistory", back_populates="stage")

    def __repr__(self) -> str:
        return f"Stages(id={self.id}, entity_id={self.entity_id}, category_id={self.category_id}, status_id={self.status_id}, name={self.name}, semantic={self.semantic})"

    # id: int = Field(..., validation_alias='ID')
    # entity_id: str = Field(..., validation_alias='ENTITY_ID')
    # category_id: int | None = Field(..., validation_alias='CATEGORY_ID')
    # status_id: str = Field(..., validation_alias='STATUS_ID')
    # name: str = Field(..., validation_alias='NAME')
    # semantic: str | None = Field(..., validation_alias='SEMANTICS')
