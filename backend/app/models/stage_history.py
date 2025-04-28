from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime, Interval, func, Column
from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from datetime import datetime, date, timedelta, time

from ..db.db import Base
from .work_calendar import WorkCalendar


class StageHistory(Base):
    __tablename__ = "stage_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    entity_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('entities.id'))
    work_order_id: Mapped[int] = mapped_column(Integer, ForeignKey('work_order.id'))
    # stage_id: Mapped[str] = mapped_column(String(255), ForeignKey('stages.status_id'))    # не можем использовать т.к. должен быть уникальным, а он бывает одинаковым
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey('stages.id'))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment='Время перевода на стадию')
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), comment='Время завершения нахождения на стадии')
    work_time: Mapped[timedelta] = mapped_column(Interval, default=timedelta(0), comment='Время на стадии, только рабочее время')
    non_work_time: Mapped[timedelta] = mapped_column(Interval, default=timedelta(0), comment='Время нахождения на стадии')

    entity = relationship("Entities", back_populates="stage_history")
    work_order = relationship("WorkOrder", back_populates="stage_history")
    stage = relationship("Stages", back_populates="stage_history")

    def __repr__(self) -> str:
        return f"<StageHistory(id={self.id}, entity_id={self.entity_id}, stage_id={self.stage_id}, start_time={self.start_time}, end_time={self.end_time})>"


async def calculate_work_time(session: AsyncSession, start_time: datetime, end_time: datetime) -> timedelta:
    if start_time is None or end_time is None:
        return timedelta(0)

    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=datetime.timezone.utc)
    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=datetime.timezone.utc)

    work_time = timedelta(0)
    current_time = start_time

    while current_time < end_time:
        day_end = datetime.combine(current_time.date(), time(23, 59, 59)).replace(tzinfo=current_time.tzinfo)
        # day_end = datetime.combine(current_time.date(), time(23, 59, 59))

        # work_calendar = (
        #     session.query(WorkCalendar)
        #     .filter(WorkCalendar.date == current_time.date())
        #     .first()
        # )
        result = await session.execute(
            select(WorkCalendar)
            .filter(WorkCalendar.date == current_time.date())
        )
        work_calendar = result.scalars().first()

        if work_calendar and work_calendar.is_working_day:
            work_start = datetime.combine(current_time.date(), work_calendar.work_start).replace(tzinfo=current_time.tzinfo)
            work_end = datetime.combine(current_time.date(), work_calendar.work_end).replace(tzinfo=current_time.tzinfo)

            # work_start = datetime.combine(current_time.date(), work_calendar.work_start)
            # work_end = datetime.combine(current_time.date(), work_calendar.work_end)

            if current_time < work_start:
                current_time = work_start
            elif current_time >= work_end:
                current_time = day_end + timedelta(seconds=1)
            else:
                work_time += min(work_end, end_time) - current_time
                current_time = min(work_end, end_time)
        else:
            current_time = day_end + timedelta(seconds=1)

    return work_time


async def update_stage_durations(session: AsyncSession, stage_history: StageHistory):
    if not session:
        raise RuntimeError("Сессия не найдена для объекта")

    print('stage_history = ', stage_history)

    if stage_history and stage_history.start_time is not None and stage_history.end_time is not None:
        print('stage_history.start_time = ', stage_history.start_time)
        print('stage_history.end_time = ', stage_history.end_time)

        work_time = await calculate_work_time(session, stage_history.start_time, stage_history.end_time)
        non_work_time = (stage_history.end_time - stage_history.start_time) - work_time

        stage_history.work_time = work_time
        stage_history.non_work_time = non_work_time
        
        await session.flush()



























# async def before_stage_history_change(mapper, connection, target):
#     session = inspect(target).async_session

#     if not session:
#         raise RuntimeError("Сессия не найдена для объекта")

#     if target.start_time is not None and target.end_time is not None:
#         work_time = await calculate_work_time(session, target.start_time, target.end_time)
#         non_work_time = (target.end_time - target.start_time) - work_time

#         target.work_time = work_time
#         target.non_work_time = non_work_time
        
#         await session.flush()

# event.listen(StageHistory, "before_update", before_stage_history_change)
