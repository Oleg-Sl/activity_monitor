import datetime
from datetime import datetime, timezone
from sqlalchemy import insert, select, update
from sqlalchemy import and_
from typing import Annotated, Dict, List

from app.models.production_schedule import ProductionSchedule
from app.models.stage import Stages
from app.models.stage_history import StageHistory
from app.repositories.base import AbstractRepository
from sqlalchemy.exc import SQLAlchemyError
# from app.parameters.params import KANBAN_ITEMS, BASE_URL


class ProductionScheduleRepository(AbstractRepository):
    async def add_one(self, data: dict) -> int:
        try:
            stmt = insert(ProductionSchedule).values(**data).returning(ProductionSchedule.id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка при добавлении: {e}")
            raise

    async def edit_one(self, id: int, data: dict) -> int:
        try:
            stmt = update(ProductionSchedule).where(ProductionSchedule.id == id).values(**data).returning(ProductionSchedule.id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка при редактировании: {e}")
            raise

    async def filter(self, *args):
        stmt = select(ProductionSchedule).where(and_(*args)).order_by(
            ProductionSchedule.priority.is_(None),
            ProductionSchedule.production_date  
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get(self, production_order_id: int) -> ProductionSchedule:
        stmt = select(ProductionSchedule).where(ProductionSchedule.id == production_order_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def find_all(self) -> List[ProductionSchedule]:
        stmt = select(ProductionSchedule)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # async def create_or_update(self, data: dict) -> int:
    #     new_stage_id = await self._get_stage_by_id_str(data['stage_id_str'])
    #     if new_stage_id is not None:
    #         data['stage_id'] = new_stage_id

    #     old_production_schedule = await self.get(data['id'])

    #     old_stage_id = None
    #     if old_production_schedule:
    #         old_stage_id = old_production_schedule.stage_id

    #     if not old_production_schedule:
    #         stmt = insert(ProductionSchedule).values(**data).returning(ProductionSchedule).execution_options(synchronize_session="fetch")
    #     else:
    #         stmt = update(ProductionSchedule).where(ProductionSchedule.id == data['id']).values(**data).returning(ProductionSchedule).execution_options(synchronize_session="fetch")

    #     result = await self.session.execute(stmt)
    #     await self.session.flush()
    #     new_production_order = result.scalar_one()

    # async def create_or_update(self, data: dict) -> int:
    #     try:
    #         new_stage_id = await self._get_stage_by_id_str(data['stage_id_str'])
    #         if new_stage_id is not None:
    #             data['stage_id'] = new_stage_id

    #         old_production_order = await self.get(data['id'])

    #         old_stage_id = None
    #         if old_production_order:
    #             old_stage_id = old_production_order.stage_id

    #         if not old_production_order:
    #             stmt = insert(ProductionOrder).values(**data).returning(ProductionOrder).execution_options(synchronize_session="fetch")
    #         else:
    #             stmt = update(ProductionOrder).where(ProductionOrder.id == data['id']).values(**data).returning(ProductionOrder).execution_options(synchronize_session="fetch")

    #         result = await self.session.execute(stmt)
    #         await self.session.flush()
    #         new_production_order = result.scalar_one()

    #         # добавление записи в историю изменения стадий
    #         # await save_stage_history(self.session, new_row, old_row_data)

    #         await self.session.commit()

    #         return new_production_order.id
    #     except SQLAlchemyError as e:
    #         await self.session.rollback()
    #         print(f"Ошибка в create_or_update: {e}")
    #         raise

    # async def _get_stage_by_id_str(self, stage_id_str: str):
    #     stmt = select(Stages.id).where(Stages.status_id == stage_id_str)
    #     result = await self.session.execute(stmt)
    #     stage_id = result.scalar_one_or_none()
    #     return stage_id