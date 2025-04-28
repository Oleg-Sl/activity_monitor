import datetime
from datetime import datetime, timezone
from sqlalchemy import insert, select, update
from sqlalchemy import and_
from typing import Annotated, Dict

from app.models.work_order import WorkOrder, save_stage_history
from app.models.stage import Stages
from app.models.stage_history import StageHistory
from app.repositories.base import AbstractRepository
from sqlalchemy.exc import SQLAlchemyError
from app.parameters.params import KANBAN_ITEMS, BASE_URL


class WorkOrderRepository(AbstractRepository):
    async def add_one(self, data: dict) -> int:
        try:
            stmt = insert(WorkOrder).values(**data).returning(WorkOrder.id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка при добавлении: {e}")
            raise

    async def edit_one(self, id: int, data: dict) -> int:
        try:
            stmt = update(WorkOrder).where(WorkOrder.id == id).values(**data).returning(WorkOrder.id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка при редактировании: {e}")
            raise

    async def filter(self, *args):
        stmt = select(WorkOrder).where(and_(*args))
        result = await self.session.execute(stmt)
        # return result.scalar_one_or_none()
        return result.scalars().all()


    async def find_all(self):
        stmt = select(WorkOrder)
        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def create_or_update(self, data: dict) -> int:
        # print('# Получение записи, если она уже сохранена в БД: ', data)
        try:
            # Поиск stage_id по его текстовому представлению
            stmt = select(Stages.id).where(Stages.status_id == data['stage_id_str'])
            result = await self.session.execute(stmt)
            stage_id = result.scalar_one_or_none()
            # print('>>> data = ', data)
            # print('>>> stage_id = ', stage_id)
            if stage_id is not None:
                data['stage_id'] = stage_id

            # Получение записи, если она уже сохранена в БД
            stmt = select(WorkOrder).where(WorkOrder.id == data['id'])
            result = await self.session.execute(stmt)
            old_row = result.scalars().first()

            old_row_data = None
            if old_row:
                old_row_data = {
                    "stage_id": old_row.stage_id
                }

            # Добавление/обновление мущности производства
            if not old_row:
                stmt = insert(WorkOrder).values(**data).returning(WorkOrder).execution_options(synchronize_session="fetch")
            else:
                stmt = update(WorkOrder).where(WorkOrder.id == data['id']).values(**data).returning(WorkOrder).execution_options(synchronize_session="fetch")

            result = await self.session.execute(stmt)
            # await self.session.commit()
            await self.session.flush()
            new_row = result.scalar_one()

            # print('old_row >>> ', old_row_data)
            # print('new_row >>> ', new_row)

            # добавление записи в историю изменения стадий
            await save_stage_history(self.session, new_row, old_row_data)

            await self.session.commit()

            return new_row.id
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка в create_or_update: {e}")
            raise

    async def get_grouped_by_kanban(self) -> Dict[str, list]:
        result = {key: [] for key in KANBAN_ITEMS}
        now = datetime.now(timezone.utc)

        all_status_ids = sum((v['status_id'] for v in KANBAN_ITEMS.values()), [])
        print('all_status_ids = ', all_status_ids)

        entities = await self.filter(WorkOrder.stage_id_str.in_(all_status_ids))
        print('entities = ', entities)
        for entity in entities:
            current_group = None
            for group_key, group_data in KANBAN_ITEMS.items():
                if entity.stage_id_str in group_data['status_id']:
                    current_group = group_key
                    break

            if current_group is None:
                continue
            
            print('entity.id = ', entity.id)

            stmt = select(StageHistory).where(
                StageHistory.work_order_id == entity.id,
                StageHistory.end_time.is_(None)
            )
            stage_result = await self.session.execute(stmt)
            print(stage_result)
            current_stage = stage_result.scalars().first()
            print('current_stage = ', current_stage)
            total_time = None
            if current_stage:
                total_time = now - current_stage.start_time

            kanban_code = KANBAN_ITEMS.get(current_group, {}).get('code')
            result[current_group].append({
                "id": entity.id,
                # "title": entity.title,
                "name": entity.name,
                "allocated_hours": entity.allocated_hours,
                # "allocated_hours": getattr(entity, f'allocated_hours_{kanban_code}', None),
                "stage_id": entity.stage_id,
                "stage_str": entity.stage_id_str,
                "stage_duration_seconds": total_time.total_seconds() if total_time else None,
                "stage_duration_hours": total_time.total_seconds() / 3600 if total_time else None,
                # "stage_duration_human": str(total_time) if total_time else None,
                "fabric_arrival_date": entity.fabric_arrival_date,
                "image": f'{BASE_URL}/static/{entity.image_local_path}'
                # "created_time": entity.created_time.date().isoformat(),
                # "updated_time": entity.updated_time.date().isoformat(),
                # "image": entity.image
            })

        return result

    async def get_grouped_by_kanban1(self) -> Dict[str, list]:
        result = {key: [] for key in KANBAN_ITEMS}
        now = datetime.now(timezone.utc)

        all_status_ids = sum((v['status_id'] for v in KANBAN_ITEMS.values()), [])

        entities = await self.filter(WorkOrder.stage_id_str.in_(all_status_ids))

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
                "fabric_arrival_date": entity.fabric_arrival_date,
                "created_time": entity.created_time.date().isoformat(),
                "updated_time": entity.updated_time.date().isoformat(),
                "image": entity.image
            })

        return result
