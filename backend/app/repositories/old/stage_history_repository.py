from sqlalchemy import insert, select, update, and_

from app.repositories.base import AbstractRepository
from app.models.stage_history import StageHistory


class StageHistoryRepository(AbstractRepository):
    async def add_one(self, data: dict) -> int:
        stmt = insert(StageHistory).values(**data).returning(StageHistory.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def edit_one(self, ident: int, data: dict) -> int:
        stmt = update(StageHistory).values(**data).filter_by(id=ident).returning(StageHistory.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()
    
    async def get(self, ident: int):
        stmt = select(StageHistory).where(StageHistory.id == ident)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def filter(self, *args):
        stmt = select(StageHistory).where(and_(*args))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all(self):
        stmt = select(StageHistory)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def log_stage_change(
        self,
        entity_type_id,
        production_order_id,
        production_schedule_id,
        old_stage_id,
        new_stage_id,
        moved_date
    ):
        # if old_stage_id == new_stage_id:
        #     return
        
        result = await self.session.execute(
            select(StageHistory)
            .filter(StageHistory.production_order_id == production_order_id)
            .order_by(StageHistory.start_time.desc())
        )
        
        old_stage_history = result.scalars().first()
        if old_stage_history and old_stage_history.stage_id != new_stage_id:
            old_stage_history.end_time = moved_date
            await self.session.flush()
        
        new_stage_history = await self.add_one({
            'entity_type_id': entity_type_id,
            'production_order_id': production_order_id,
            'stage_id': new_stage_id,
            'start_time': moved_date
        })
        return new_stage_history