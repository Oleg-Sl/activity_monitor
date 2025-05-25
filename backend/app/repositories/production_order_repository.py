import datetime
from datetime import datetime, timezone
from sqlalchemy import insert, select, update
from sqlalchemy import and_
from typing import Annotated, Dict, List

from app.models.production_order import ProductionOrder
from app.models.stage import Stages
from app.models.stage_history import StageHistory
from app.models.production_stage_history import ProductionStageHistory
from app.repositories.base import AbstractRepository
from sqlalchemy.exc import SQLAlchemyError
# from app.parameters.params import KANBAN_ITEMS, BASE_URL


class ProductionOrderRepository(AbstractRepository):
    async def add_one(self, data: dict) -> int:
        try:
            stmt = insert(ProductionOrder).values(**data).returning(ProductionOrder.id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка при добавлении: {e}")
            raise

    async def edit_one(self, id: int, data: dict) -> int:
        try:
            stmt = update(ProductionOrder).where(ProductionOrder.id == id).values(**data).returning(ProductionOrder.id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка при редактировании: {e}")
            raise

    async def filter(self, *args):
        stmt = select(ProductionOrder).where(and_(*args)).order_by(ProductionOrder.production_date)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get(self, production_order_id: int) -> ProductionOrder:
        stmt = select(ProductionOrder).where(ProductionOrder.id == production_order_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def find_all(self) -> List[ProductionOrder]:
        stmt = select(ProductionOrder)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def flush(self):
        await self.session.flush()

    async def commit(self):
        await self.session.commit()

    async def create_or_update(self, data: dict) -> int:
        new_stage_id = await self._get_stage_by_id_str(data['stage_id_str'])
        if new_stage_id is not None:
            data['stage_id'] = new_stage_id

        old_production_order = await self.get(data['id'])

        old_stage_id = None
        if old_production_order:
            old_stage_id = old_production_order.stage_id

        if not old_production_order:
            stmt = insert(ProductionOrder).values(**data).returning(ProductionOrder).execution_options(synchronize_session="fetch")
        else:
            stmt = update(ProductionOrder).where(ProductionOrder.id == data['id']).values(**data).returning(ProductionOrder).execution_options(synchronize_session="fetch")

        result = await self.session.execute(stmt)
        await self.session.flush()
        new_production_order = result.scalar_one()


    async def get_completed(self, stage_ids_str: List[str], week_start, week_end):
        stmt = select(ProductionOrder).join(ProductionStageHistory).where(
            and_(
                ProductionStageHistory.stage_id_str.in_(stage_ids_str),
                ProductionStageHistory.moved_time >= week_start,
                ProductionStageHistory.moved_time <= week_end,
                ProductionOrder.stage_id_str.not_in(stage_ids_str)
            )
        ).order_by(ProductionOrder.production_date)
        result = await self.session.execute(stmt)
        return result.scalars().all()

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

    async def _get_stage_by_id_str(self, stage_id_str: str):
        stmt = select(Stages.id).where(Stages.status_id == stage_id_str)
        result = await self.session.execute(stmt)
        stage_id = result.scalar_one_or_none()
        return stage_id