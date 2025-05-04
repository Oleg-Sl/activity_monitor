import asyncio
from typing import List, Optional
from sqlalchemy import event
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy import inspect
from sqlalchemy import Integer, String, Float, Date, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from datetime import datetime, date

from ..db.db import Base
from .stage_history import StageHistory, update_stage_durations
# from .stage import Stages


class WorkOrder(Base):
    __tablename__ = 'work_order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Идентификатор в Битрикс")
    title: Mapped[Optional[str]] = mapped_column(String(255), comment="Название смарт-процесса в Битрикс")
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Когда создан")
    updated_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Когда обновлён")
    created_by: Mapped[int] = mapped_column(Integer, comment="Кем создан")
    assigned_by_id: Mapped[int] = mapped_column(Integer, comment="Ответственный")
    company_id: Mapped[Optional[int]] = mapped_column(Integer, comment="Компания")
    category_id: Mapped[Optional[int]] = mapped_column(Integer, comment="Воронка")

    moved_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Когда передвинут")
    moved_by: Mapped[int] = mapped_column(Integer, comment="Кем передвинут")
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey('stages.id'), comment="Стадия")
    stage_id_str: Mapped[str] = mapped_column(String(255), comment="Стадия абревиатура")
    previous_stage_id: Mapped[str] = mapped_column(String(255), comment="Предыдущая стадия")

    opportunity: Mapped[Optional[float]] = mapped_column(Float, comment="Сумма")
    product_id: Mapped[Optional[int]] = mapped_column(Integer, comment="ID_изделия_смарт")
    product_type: Mapped[Optional[int]] = mapped_column(Integer, comment="Тип изделия")

    fabric_arrival_date: Mapped[Optional[str]] = mapped_column(String(255), comment="Дата прихода ткани")

    name: Mapped[Optional[str]] = mapped_column(String(255), comment="Имя изделия")
    product_type_str: Mapped[Optional[str]] = mapped_column(String(255), comment="Аббревиатура типа изделия")

    image_url: Mapped[Optional[str]] = mapped_column(String(2048), comment="url фотографии")
    image_token: Mapped[Optional[str]] = mapped_column(String(2048), comment="Уникальный токен фотографии изделия (из url)")
    image_local_path: Mapped[Optional[str]] = mapped_column(String(255), comment="Путь к фотографии на сервере")

    allocated_hours: Mapped[Optional[float]] = mapped_column(Float, comment="Выделено часов на стадии")

    stage_history = relationship("StageHistory", back_populates="work_order")

    def __repr__(self):
        return (
            f"<WorkOrder(id={self.id}, "
            f"title='{self.title}', "
            f"stage_id_str='{self.stage_id_str}', "
            f"name='{self.name}')>"
        )

async def save_stage_history(session: AsyncSession, new_entity: WorkOrder, old_entity: dict):
    # print('new_entity = ', new_entity)
    # print('old_entity = ', old_entity)
    if old_entity is not None and new_entity.stage_id == old_entity['stage_id']:
        return

    result = await session.execute(
        select(StageHistory)
        # .filter(StageHistory.entity_id == new_entity.id)
        .filter(StageHistory.work_order_id == new_entity.id)
        .order_by(StageHistory.start_time.desc())
    )
    last_history_stage = result.scalars().first()

    print('last_history_stage = ', last_history_stage)

    # добавляем к последней записи в истории время завершения нахождения на стадии
    if last_history_stage:
        last_history_stage.end_time = new_entity.updated_time
        await session.flush()

    # добавление записи перехода на новую стадию
    new_history_entry = StageHistory(
        # entity_id=new_entity.id,
        work_order_id=new_entity.id,
        stage_id=new_entity.stage_id,
        start_time=new_entity.updated_time,
    )
    session.add(new_history_entry)

    await update_stage_durations(session, last_history_stage)


# alembic revision --autogenerate -m "initial"
# alembic revision --autogenerate -m "Add fields to entity model"
# alembic upgrade head
