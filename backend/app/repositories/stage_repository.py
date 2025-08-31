import datetime
from sqlalchemy import insert, select, update
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.base import AbstractRepository
from app.models.stage import Stages


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

    async def get(self, ident: int):
        stmt = select(Stages).where(Stages.id == ident)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_status_id(self, ident_str: int):
        stmt = select(Stages).where(Stages.status_id == ident_str)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

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
