from sqlalchemy import insert, select, update, and_

from app.repositories.base import AbstractRepository
from app.models.work_calendar import WorkCalendar


class WorkCalendarRepository(AbstractRepository):
    async def add_one(self, data: dict) -> int:
        stmt = insert(WorkCalendar).values(**data).returning(WorkCalendar.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def edit_one(self, ident: int, data: dict) -> int:
        stmt = update(WorkCalendar).values(**data).filter_by(id=ident).returning(WorkCalendar.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()
    
    async def get(self, ident: int):
        stmt = select(WorkCalendar).where(WorkCalendar.id == ident)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def filter(self, *args):
        stmt = select(WorkCalendar).where(and_(*args))
        result = await self.session.execute(stmt)
        # return result.scalar_one_or_none()
        return result.scalars().all()

    async def find_all(self):
        stmt = select(WorkCalendar)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_if_not_exist(self, data: dict) -> int:
        stmt = select(WorkCalendar).where(WorkCalendar.date == data['date'])
        result = await self.session.execute(stmt)
        day = result.scalars().first()
        if not day:
            stmt = insert(WorkCalendar).values(**data).returning(WorkCalendar.id)
            result = await self.session.execute(stmt)
            return result.scalar_one()
