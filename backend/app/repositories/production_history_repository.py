from sqlalchemy import insert, select, update, and_

from app.repositories.base import AbstractRepository
from app.models.production_stage_history import ProductionStageHistory


class ProductionHistoryRepository(AbstractRepository):
    async def add_one(self, data: dict) -> int:
        stmt = insert(ProductionStageHistory).values(**data).returning(ProductionStageHistory.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def edit_one(self, ident: int, data: dict) -> int:
        stmt = update(ProductionStageHistory).values(**data).filter_by(id=ident).returning(ProductionStageHistory.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()
    
    async def get(self, ident: int):
        stmt = select(ProductionStageHistory).where(ProductionStageHistory.id == ident)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def filter(self, *args):
        stmt = select(ProductionStageHistory).where(and_(*args))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all(self):
        stmt = select(ProductionStageHistory)
        result = await self.session.execute(stmt)
        return result.scalars().all()

