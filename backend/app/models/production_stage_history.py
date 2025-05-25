from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, DateTime, Interval, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta, time

from app.db.session import Base


class ProductionStageHistory(Base):
    __tablename__ = "production_stage_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    production_order_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('production_order.id'))
    stage_id_str: Mapped[str] = mapped_column(String(255), comment="Стадия - абревиатура")
    moved_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Когда передвинут")

    # production_order = relationship("ProductionOrder", back_populates="stage_histories")


# alembic revision --autogenerate -m "initial"
# alembic revision --autogenerate -m "Add table of stage histories"
# alembic upgrade head





















