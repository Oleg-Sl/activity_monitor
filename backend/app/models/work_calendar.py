from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Date, DateTime, Interval, Boolean, Time
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import datetime

from ..db.db import Base


class WorkCalendar(Base):
    __tablename__ = "work_calendar"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, unique=True)
    is_working_day: Mapped[bool] = mapped_column(Boolean, default=True)
    work_start: Mapped[datetime.time | None] = mapped_column(Time)
    work_end: Mapped[datetime.time | None] = mapped_column(Time)
    description: Mapped[str] = mapped_column(String(255), default="")

    def __repr__(self) -> str:
        return f"<WorkCalendar(id={self.id}, date={self.date}, description={self.description})>"
