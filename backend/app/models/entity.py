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
from .stage import Stages


class Entities(Base):
    __tablename__ = 'entities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="")
    title: Mapped[Optional[str]] = mapped_column(String(255))
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Когда создан")
    updated_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Когда обновлён")
    created_by: Mapped[int] = mapped_column(Integer, comment="Кем создан")
    assigned_by_id: Mapped[int] = mapped_column(Integer, comment="Ответственный")
    company_id: Mapped[Optional[int]] = mapped_column(Integer, comment="Компания")
    category_id: Mapped[Optional[int]] = mapped_column(Integer, comment="Воронка")

    moved_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Когда передвинут")
    moved_by: Mapped[int] = mapped_column(Integer, comment="Кем передвинут")
    # stage_id: Mapped[int] = mapped_column(Integer, description="Стадия")
    # stage_id: Mapped[str] = mapped_column(String(255), ForeignKey('stages.status_id'), comment="Стадия")    # не можем использовать т.к. должен быть уникальным, а он бывает одинаковым
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey('stages.id'), comment="Стадия")
    stage_id_str: Mapped[str] = mapped_column(String(255), comment="Стадия абревиатура")
    previous_stage_id: Mapped[str] = mapped_column(String(255), comment="Предыдущая стадия")

    opportunity: Mapped[Optional[float]] = mapped_column(Float, comment="Сумма")
    product_id: Mapped[Optional[int]] = mapped_column(Integer, comment="ID_изделия_смарт")
    product_type: Mapped[Optional[int]] = mapped_column(Integer, comment="Тип изделия")

    zakup_id: Mapped[Optional[int]] = mapped_column(Integer, comment="ID смарта закупки")
    fabric_arrival_date: Mapped[Optional[str]] = mapped_column(String(255), comment="Дата прихода ткани")

    name: Mapped[Optional[str]] = mapped_column(String(255), comment="Имя изделия")
    product_type_str: Mapped[Optional[str]] = mapped_column(String(255), comment="Аббревиатура типа изделия")
    image: Mapped[Optional[str]] = mapped_column(String(2048), comment="Фото изделия")
    image: Mapped[Optional[str]] = mapped_column(String(2048), comment="Фото изделия")
    # original_url = Column(String, nullable=False)
    # local_url = Column(String, nullable=False)
    fot_id: Mapped[Optional[int]] = mapped_column(Integer, comment="ID смарта фот")

    allocated_hours_development: Mapped[Optional[int]] = mapped_column(Integer, comment="Разработка - выделено часов")
    allocated_hours_sawing: Mapped[Optional[int]] = mapped_column(Integer, comment="Пилка - выделено часов")
    allocated_hours_assembly: Mapped[Optional[int]] = mapped_column(Integer, comment="Сборка - выделено часов")
    allocated_hours_ppu: Mapped[Optional[int]] = mapped_column(Integer, comment="ППУ - выделено часов")
    allocated_hours_sewing: Mapped[Optional[int]] = mapped_column(Integer, comment="Швейка - выделено часов")
    allocated_hours_covering: Mapped[Optional[int]] = mapped_column(Integer, comment="Обтяжка - выделено часов")
    allocated_hours_carpentry: Mapped[Optional[int]] = mapped_column(Integer, comment="Столярка - выделено часов")
    allocated_hours_carpentry_assembly: Mapped[Optional[int]] = mapped_column(Integer, comment="Столярка (сборка) - выделено часов")
    allocated_hours_painting_preparation: Mapped[Optional[int]] = mapped_column(Integer, comment="Покраска (подготовка) - выделено часов")
    allocated_hours_painting: Mapped[Optional[int]] = mapped_column(Integer, comment="Покраска - выделено часов")

    stage_history = relationship("StageHistory", back_populates="entity")


    # parent_deal: Mapped[float | None] = mapped_column(Float, description="Сделка")

    # item_ready_date: Mapped[date | None] = mapped_column(Date, description="Дата приема готовности изделия")
    # pack_date: Mapped[date | None] = mapped_column(Date, description="Дата упаковки")
    # item_id: Mapped[int | None] = mapped_column(Integer, description="ID_товарной позиции")
    # cost_price: Mapped[float | None] = mapped_column(Float, description="Себестоимость изделия")

    # shop_entry_date: Mapped[date | None] = mapped_column(Date, description="Дата поступления в цех")
    # design_end_date: Mapped[date | None] = mapped_column(Date, description="Дата завершения проектирования")
    # contract_due_date: Mapped[date | None] = mapped_column(Date, description="Дата сдачи по договору")

    # agreed_log_date: Mapped[datetime | None] = mapped_column(DateTime, description="Дата логистика (согласованная)")
    # actual_ship_date: Mapped[date | None] = mapped_column(Date, description="Дата фактической отгрузки")
    # forecast_ready_date: Mapped[date | None] = mapped_column(Date, description="Дата ПРОГНОЗ готовности")
    # work_start_date: Mapped[datetime | None] = mapped_column(DateTime, description="Дата старта (принят в работу)")

    def __repr__(self):
        return f"<BitrixEntity(id={self.id}, title={self.title}, created_time={self.created_time}, stage_id_str={self.stage_id_str}, stage_id={self.stage_id})>"


async def save_stage_history(session: AsyncSession, new_entity: Entities, old_entity: dict):
    print('new_entity = ', new_entity)
    print('old_entity = ', old_entity)
    if old_entity is not None and new_entity.stage_id == old_entity['stage_id']:
        return

    result = await session.execute(
        select(StageHistory)
        .filter(StageHistory.entity_id == new_entity.id)
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
        entity_id=new_entity.id,
        stage_id=new_entity.stage_id,
        start_time=new_entity.updated_time,
    )
    session.add(new_history_entry)

    await update_stage_durations(session, last_history_stage)

  
    # await session.flush()
    # session.add(new_history_entry)
    # await self.session.commit()


# alembic revision --autogenerate -m "initial"
# alembic revision --autogenerate -m "Add fields to entity model"
# alembic upgrade head






















# def save_stage_history(connection, new_entity, old_entity):
#     # стадия не изменилась (не сохраняем в истории)
#     if old_entity is not None and new_entity.stage_id == old_entity.stage_id:
#         return

#     last_history_stage = connection.execute(
#         text("SELECT * FROM stage_history WHERE entity_id = :entity_id ORDER BY start_time DESC LIMIT 1"),
#         {"entity_id": new_entity.id}
#     ).fetchone()

#     if last_history_stage:
#         last_history_stage.end_time = new_entity.updated_time

#     connection.execute(
#         text("INSERT INTO stage_history (entity_id, stage_id, start_time) VALUES (:entity_id, :stage_id, :start_time)"),
#         {"entity_id": new_entity.id, "stage_id": new_entity.stage_id, "start_time": new_entity.updated_time}
#     )

# async def save_stage_history(session: AsyncSession, new_entity: Entities, old_entity: Entities):
#     if old_entity is not None and new_entity.stage_id == old_entity.stage_id:
#         return
#     print("!!!!!new_entity = ", new_entity)
#     result = await session.execute(
#         select(StageHistory)
#         .filter(StageHistory.entity_id == new_entity.id)
#         .order_by(StageHistory.start_time.desc())
#     )
#     last_history_stage = result.scalars().first()
#     # last_history_stage = (
#     #     session.query(StageHistory)
#     #     .filter(StageHistory.entity_id == new_entity.id)
#     #     .order_by(StageHistory.start_time.desc())
#     #     .first()
#     # )

#     # добавляем к последней записи в истории время завершения нахождения на стадии
#     if last_history_stage:
#         last_history_stage.end_time = new_entity.updated_time

#     # добавление записи перехода на новую стадию
#     new_history_entry = StageHistory(
#         entity_id=new_entity.id,
#         stage_id=new_entity.stage_id,
#         start_time=new_entity.updated_time,
#     )
#     session.add(new_history_entry)
#     await session.flush()
#     # session.add(new_history_entry)


# async def before_entity_change(mapper, connection, target):
#     print('+'*88)
    # session = Session.object_session(target)
    # session = inspect(target).session
    # session = inspect(target).async_session

    # old_entity = None
    # if target.id:
    #     print('2'*88)
    #     result = await session.execute(select(Entities).filter(Entities.id == target.id))
    #     old_entity = result.scalars().first()
    # print('3'*88)
    # await save_stage_history(session, target, old_entity)
    # if target.id:
    #     old_entity = connection.execute(
    #         text("SELECT * FROM entities WHERE id = :id"),
    #         {"id": target.id}
    #     ).fetchone()
    # save_stage_history(connection, target, old_entity)

# def validate_phone(target, value, oldvalue, initiator):
#     """Strip non-numeric characters from a phone number"""
#     print('-'*88)
#     return 1


# setup listener on UserContact.phone attribute, instructing
# it to use the return value
# event.listen(Entities.stage_id, "set", validate_phone, retval=True)

# event.listen(Entities, "before_insert", before_entity_change)
# event.listen(Entities, "before_update", before_entity_change)
# async def handle_event(mapper, connection, target):
#     await before_entity_change(mapper, connection, target)

# # Регистрация события для перед вставкой и перед обновлением
# event.listen(Entities, "before_insert", lambda mapper, connection, target: asyncio.run(handle_event(mapper, connection, target)))
# event.listen(Entities, "before_update", lambda mapper, connection, target: asyncio.run(handle_event(mapper, connection, target)))
