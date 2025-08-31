from sqlalchemy import insert, select, update

from app.models.work_calendar import WorkCalendar
from app.repositories.base import AbstractRepository
import datetime

class WorkCalendarRepository(AbstractRepository):
    async def add_one(self, data: dict) -> int:
        stmt = insert(WorkCalendar).values(**data).returning(WorkCalendar.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def get_by_date(self, date: datetime.date) -> int:
        stmt = select(WorkCalendar).where(WorkCalendar.date==date)
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = update(WorkCalendar).values(**data).filter_by(id=id).returning(WorkCalendar.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

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
