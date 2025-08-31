import datetime
from sqlalchemy import insert, select, update
from sqlalchemy import and_

from app.models.stage import Stages
from app.repositories.base import AbstractRepository
from sqlalchemy.exc import SQLAlchemyError


class StageRepository(AbstractRepository):    
    async def add_one(self, data: dict) -> int:
        try:
            stmt = insert(Stages).values(**data).returning(Stages.id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка при добавлении: {e}")
            raise

    async def edit_one(self, id: int, data: dict) -> int:
        try:
            stmt = update(Stages).where(Stages.id == id).values(**data).returning(Stages.id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка при редактировании: {e}")
            raise

    async def filter(self, *args):
        stmt = select(Stages).where(and_(*args))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all(self):
        stmt = select(Stages)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def create_or_update(self, data: dict) -> int:
        try:
            stmt = select(Stages).where(Stages.id == data['id'])
            result = await self.session.execute(stmt)
            row = result.scalars().first()

            if not row:
                stmt = insert(Stages).values(**data).returning(Stages.id)
            else:
                stmt = update(Stages).where(Stages.id == data['id']).values(**data).returning(Stages.id)

            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка в create_or_update: {e}")
            raise
