import datetime
from datetime import datetime, timezone
from sqlalchemy import insert, select, update
from sqlalchemy import and_
from typing import Annotated, Dict

from app.models.entity import Entities, save_stage_history
from app.models.stage import Stages
from app.models.stage_history import StageHistory
from app.repositories.base import AbstractRepository
from sqlalchemy.exc import SQLAlchemyError
from app.parameters.params import KANBAN_ITEMS


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
        # return result.scalar_one_or_none()
        return result.scalars().all()


    async def find_all(self):
        stmt = select(Entities)
        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def create_or_update(self, data: dict) -> int:
        # print('# Получение записи, если она уже сохранена в БД: ', data)
        try:
            stmt = select(Stages.id).where(Stages.status_id == data['stage_id_str'])
            result = await self.session.execute(stmt)
            stage_id = result.scalar_one_or_none()
            print('>>> data = ', data)
            print('>>> stage_id = ', stage_id)
            if stage_id is not None:
                data['stage_id'] = stage_id

            # Получение записи, если она уже сохранена в БД
            stmt = select(Entities).where(Entities.id == data['id'])
            result = await self.session.execute(stmt)
            old_row = result.scalars().first()

            # создание или обновление записи
            # if not old_row:
            #     stmt = insert(Entities).values(**data).returning(Entities.id)
            # else:
            #     stmt = update(Entities).where(Entities.id == data['id']).values(**data).returning(Entities.id)

            old_row_data = None
            if old_row:
                old_row_data = {
                    "stage_id": old_row.stage_id
                }

            if not old_row:
                stmt = insert(Entities).values(**data).returning(Entities).execution_options(synchronize_session="fetch")
            else:
                stmt = update(Entities).where(Entities.id == data['id']).values(**data).returning(Entities).execution_options(synchronize_session="fetch")

            result = await self.session.execute(stmt)
            # await self.session.commit()
            await self.session.flush()
            new_row = result.scalar_one()

            print('old_row >>> ', old_row_data)
            print('new_row >>> ', new_row)

            # добавление записи в историю изменения стадий
            await save_stage_history(self.session, new_row, old_row_data)

            await self.session.commit()

            return new_row.id
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка в create_or_update: {e}")
            raise

    async def get_grouped_by_kanban(self) -> Dict[str, list]:
        result = {key: {} for key in KANBAN_ITEMS}
        now = datetime.now(timezone.utc)

        all_status_ids = sum((v['status_id'] for v in KANBAN_ITEMS.values()), [])

        entities = await self.filter(Entities.stage_id_str.in_(all_status_ids))

        for entity in entities:
            current_group = None
            for group_key, group_data in KANBAN_ITEMS.items():
                if entity.stage_id_str in group_data['status_id']:
                    current_group = group_key
                    break

            if current_group is None:
                continue

            stmt = select(StageHistory).where(
                StageHistory.entity_id == entity.id,
                StageHistory.end_time.is_(None)
            )
            stage_result = await self.session.execute(stmt)
            current_stage = stage_result.scalars().first()

            total_time = None
            if current_stage:
                total_time = now - current_stage.start_time

            kanban_code = KANBAN_ITEMS.get(current_group, {}).get('code')
            result[current_group].append({
                "id": entity.id,
                "title": entity.title,
                "name": entity.name,
                "allocated_hours": getattr(entity, f'allocated_hours_{kanban_code}', None),
                "stage_id": entity.stage_id,
                "stage_str": entity.stage_id_str,
                "stage_duration_seconds": total_time.total_seconds() if total_time else None,
                "stage_duration_human": str(total_time) if total_time else None,
                # "fabric_arrival_date": entity.fabric_arrival_date.isoformat() if entity.fabric_arrival_date else None,
                "fabric_arrival_date": entity.fabric_arrival_date,
                "created_time": entity.created_time.date().isoformat(),
                "updated_time": entity.updated_time.date().isoformat(),
                "image": entity.image
            })

        return result








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