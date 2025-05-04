from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, DateTime, Interval, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta, time

from app.db.session import Base


class StageHistory(Base):
    __tablename__ = "stage_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    entity_type_id: Mapped[Optional[int]]
    production_order_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('production_order.id'))
    production_schedule_id: Mapped[int] = mapped_column(Integer, ForeignKey('production_schedule.id'))
    # stage_id: Mapped[str] = mapped_column(String(255), ForeignKey('stages.status_id'))    # не можем использовать т.к. должен быть уникальным, а он бывает одинаковым
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey('stages.id'))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment='Время перевода на стадию')
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), comment='Время завершения нахождения на стадии')
    work_time: Mapped[timedelta] = mapped_column(Interval, default=timedelta(0), comment='Время на стадии, только рабочее время')
    non_work_time: Mapped[timedelta] = mapped_column(Interval, default=timedelta(0), comment='Время нахождения на стадии')

    production_schedule = relationship("ProductionSchedule", back_populates="stage_histories")
    production_order = relationship("ProductionOrder", back_populates="stage_histories")
    stage = relationship("Stages", back_populates="stage_histories")

    def __repr__(self) -> str:
        return f"<StageHistory(id={self.id}, entity_id={self.entity_id}, stage_id={self.stage_id}, start_time={self.start_time}, end_time={self.end_time})>"

# alembic revision --autogenerate -m "initial"
# alembic revision --autogenerate -m "Add fields to entity model"
# alembic upgrade head
