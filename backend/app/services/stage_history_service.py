# app/services/stage_history_service.py
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.models import StageHistory
from logging import getLogger

# logger = getLogger(__name__)

class StageHistoryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_stage_change(
        self,
        order_id: int,
        new_stage_id: int,
        old_stage_id: int | None = None,
        changed_by: str | None = None,
        comment: str | None = None
    ) -> None:
        if old_stage_id == new_stage_id:
            # logger.debug(f"Стадия не изменилась для заказа {order_id}")
            return

        stmt = insert(StageHistory).values(
            order_id=order_id,
            old_stage_id=old_stage_id,
            new_stage_id=new_stage_id,
            changed_at=datetime.utcnow(),
            changed_by=changed_by,
            comment=comment
        )
        
        try:
            await self.session.execute(stmt)
            logger.info(f"Записано изменение стадии для заказа {order_id}: {old_stage_id} -> {new_stage_id}")
        except Exception as e:
            logger.error(f"Ошибка записи истории стадий: {e}")
            raise

async def save_stage_history(session: AsyncSession, new_entity: WorkOrder, old_entity: dict):
    # print('new_entity = ', new_entity)
    # print('old_entity = ', old_entity)
    if old_entity is not None and new_entity.stage_id == old_entity['stage_id']:
        return

    result = await session.execute(
        select(StageHistory)
        # .filter(StageHistory.entity_id == new_entity.id)
        .filter(StageHistory.work_order_id == new_entity.id)
        .order_by(StageHistory.start_time.desc())
    )
    last_history_stage = result.scalars().first()

    print('last_history_stage = ', last_history_stage)

    # добавляем к последней записи в истории время завершения нахождения на стадии
    if last_history_stage:
        last_history_stage.end_time = new_entity.updated_time
        await session.flush()

    # добавление записи перехода на новую стадию
    new_history_entry = StageHistory(
        # entity_id=new_entity.id,
        work_order_id=new_entity.id,
        stage_id=new_entity.stage_id,
        start_time=new_entity.updated_time,
    )
    session.add(new_history_entry)

    await update_stage_durations(session, last_history_stage)
