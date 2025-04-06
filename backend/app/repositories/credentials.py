from sqlalchemy import insert, select, update, and_

from app.models.credential import Credentials
from app.repositories.base import AbstractRepository


class CredentialRepository(AbstractRepository):
    async def add_one(self, data: dict) -> int:
        stmt = insert(Credentials).values(**data).returning(Credentials.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def edit_one(self, ident: int, data: dict) -> int:
        stmt = update(Credentials).values(**data).filter_by(id=ident).returning(Credentials.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()
    
    async def get(self, credential_id):
        stmt = select(Credentials).where(Credentials.id == credential_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def filter(self, *args):
        stmt = select(Credentials).where(and_(*args))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def find_all(self):
        stmt = select(Credentials)
        result = await self.session.execute(stmt)
        return result.scalars().all()
