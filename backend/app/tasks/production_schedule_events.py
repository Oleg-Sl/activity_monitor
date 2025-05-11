import asyncio

from app.services.bitrix24.factory import get_bitrix_client
from app.db.session import async_session_maker
from app.infrastructure.bitrix_event_client import BitrixEventFetcher
from app.services.entities.production_schedule_service import ProductionScheduleService
from app.constants.product_schedule import PRODUCTION_SCHEDULE_EVENT_NAMES
from app.repositories.production_schedule_repository import ProductionScheduleRepository
from app.repositories.stage_history_repository import StageHistoryRepository
from app.repositories.stage_repository import StageRepository
from app.repositories.work_calendar_repository import WorkCalendarRepository



# получение данных из очереди событий
async def sync_production_schedule_events_task():
    async with async_session_maker() as session:
        bitrix_client = get_bitrix_client(session)
        fetcher = BitrixEventFetcher(bitrix_client)

        production_schedule_repository = ProductionScheduleRepository(session)
        stage_history_repository = StageHistoryRepository(session)
        stage_repository = StageRepository(session)
        work_calendar_repository = WorkCalendarRepository(session)

        service = ProductionScheduleService(
            bitrix_client,
            production_schedule_repository,
            stage_history_repository,
            stage_repository,
            work_calendar_repository
        )

        # for event_name in PRODUCTION_SCHEDULE_EVENT_NAMES:
        #     async for production_schedule_ids in fetcher.fetch_events(event_name):
        #         result = await service.save_schedule_to_db(production_orders_ids)

        print('*'*88)
        # production_schedules = await service.get_production([2789, 2829, 2801,])
        # for production_schedule in production_schedules:
        #     print(production_schedule)
        await service.save_productions_to_db([2789, 2829, 2801,])


if __name__ == "__main__":
    asyncio.run(sync_production_schedule_events_task())


# python -m app.tasks.production_schedule_events
# .\venv\Scripts\activate
