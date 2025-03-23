from sqlalchemy import insert, select, update

from app.models.credential import Credentials
from app.repositories.base import AbstractRepository


class BitrixCredentialsRepository(AbstractRepository):
    async def add_one(self, data: dict) -> int:
        stmt = insert(Credentials).values(**data).returning(Credentials.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def edit_one(self, id: int, data: dict) -> int:
        stmt = update(Credentials).values(**data).filter_by(id=id).returning(Credentials.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self):
        stmt = select(Credentials)
        result = await self.session.execute(stmt)
        return result.scalars().all()
