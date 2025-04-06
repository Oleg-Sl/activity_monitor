import datetime
from sqlalchemy import insert, select, update
from sqlalchemy import and_

from app.models.entity import Entities, save_stage_history
from app.repositories.base import AbstractRepository
from sqlalchemy.exc import SQLAlchemyError


class EntityRepository(AbstractRepository):
    async def add_one(self, data: dict) -> int:
        try:
            stmt = insert(Entities).values(**data).returning(Entities.id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка при добавлении: {e}")
            raise

    async def edit_one(self, id: int, data: dict) -> int:
        try:
            stmt = update(Entities).where(Entities.id == id).values(**data).returning(Entities.id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка при редактировании: {e}")
            raise

    async def filter(self, *args):
        stmt = select(Entities).where(and_(*args))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all(self):
        stmt = select(Entities)
        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def create_or_update(self, data: dict) -> int:
        print('# Получение записи, если она уже сохранена в БД')
        try:
            # Получение записи, если она уже сохранена в БД
            stmt = select(Entities).where(Entities.id == data['id'])
            result = await self.session.execute(stmt)
            old_row = result.scalars().first()

            # создание или обновление записи
            # if not old_row:
            #     stmt = insert(Entities).values(**data).returning(Entities.id)
            # else:
            #     stmt = update(Entities).where(Entities.id == data['id']).values(**data).returning(Entities.id)

            if not old_row:
                stmt = insert(Entities).values(**data).returning(Entities).execution_options(synchronize_session="fetch")
            else:
                stmt = update(Entities).where(Entities.id == data['id']).values(**data).returning(Entities).execution_options(synchronize_session="fetch")

            result = await self.session.execute(stmt)
            await self.session.commit()
            new_row = result.scalar_one()

            # добавление записи в историю изменения стадий
            await save_stage_history(self.session, new_row, old_row)

            return new_row.id
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка в create_or_update: {e}")
            raise










    # async def create_or_update(self, data: dict) -> int:
    #     stmt = select(Entities).where(Entities.id == data['id'])
    #     result = await self.session.execute(stmt)
    #     row = result.scalars().first()

    #     if not row:
    #         stmt = insert(Entities).values(**data).returning(Entities.id)
    #     else:
    #         stmt = update(Entities).where(Entities.id == data['id']).values(**data).returning(Entities.id)

    #     result = await self.session.execute(stmt)
    #     return result.scalar_one()