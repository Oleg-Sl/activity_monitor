
import asyncio
from app.services.bitrix24.factory import get_bitrix_client
from app.db.session import async_session_maker

from app.infrastructure.bitrix_event_client import BitrixEventFetcher
from app.services.entities.production_schedule_service import ProductionScheduleService
# from app.repositories.production_schedule_repository import ProductionScheduleRepository
from app.repositories.production_order_repository import ProductionOrderRepository
from app.repositories.stage_history_repository import StageHistoryRepository
from app.repositories.work_calendar_repository import WorkCalendarRepository
from app.repositories.stage_repository import StageRepository


# получение данных из очереди событий
async def sync_production_schedules_task():
    async with async_session_maker() as session:
        bitrix_client = get_bitrix_client(session)
        fetcher = BitrixEventFetcher(bitrix_client)
        # production_repository = ProductionScheduleRepository(session)
        production_repository = ProductionOrderRepository(session)
        stage_history_repository = StageHistoryRepository(session)
        stage_repository = StageRepository(session)
        work_calendar_repository = WorkCalendarRepository(session)

        service = ProductionScheduleService(
            bitrix_client,
            production_repository,
            stage_history_repository,
            stage_repository,
            work_calendar_repository
        )

        await service.sync_production('2025-05-01', '2025-05-25')


if __name__ == "__main__":
    asyncio.run(sync_production_schedules_task())


# python -m app.tasks.production_schedule_sync
# .\venv\Scripts\activate
