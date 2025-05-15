import datetime
from typing import List, Optional
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

# from app.constants.production_order import PRODUCTION_ORDER_TYPE_OF_PRODUCT
# from app.constants.common import PRODUCTION_ORDER_TYPE_ID
# from app.core.config import BASE_DIR, BASE_URL
# from app.services.bitrix24.bitrix_client import InterfaceBitrixClient
# from app.schemas.product_order_schema import ProductOrderInSchema
# from app.infrastructure.file_downloader.file_downloader import FileDownloader
# from app.services.file_service import FileServiceFactory
# from app.repositories.production_order_repository import ProductionOrderRepository
# from app.repositories.stage_history_repository import StageHistoryRepository
# from app.repositories.work_calendar_repository import WorkCalendarRepository
# from app.repositories.stage_repository import StageRepository
# from app.models.stage import Stages
# from app.models.production_order import ProductionOrder
# from app.models.production_schedule import ProductionSchedule
# from app.repositories.production_order_repository import ProductionOrderRepository
# from app.repositories.production_schedule_repository import ProductionScheduleRepository
from app.repositories.work_calendar_repository import WorkCalendarRepository
from app.models.work_calendar import WorkCalendar


class WorkCaldendarService:
    def __init__(self, calendar_repo: WorkCalendarRepository):
        self.calendar_repo = calendar_repo

    async def calculate_work_time(self, start_time: datetime, end_time: datetime) -> datetime.timedelta:
        if start_time is None or end_time is None:
            return datetime.timedelta(0)

        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=datetime.timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=datetime.timezone.utc)

        work_time = datetime.timedelta(0)
        current_time = start_time

        while current_time < end_time:
            day_end = datetime.datetime.combine(current_time.date(), datetime.time(23, 59, 59)).replace(tzinfo=current_time.tzinfo)
            result = await self.calendar_repo.filter(WorkCalendar.date == current_time.date())
            work_calendar = None
            if result:
                work_calendar = result[0]

            # result = await session.execute(
            #     select(WorkCalendar)
            #     .filter(WorkCalendar.date == current_time.date())
            # )
            # work_calendar = result.scalars().first()

            if work_calendar and work_calendar.is_working_day:
                work_start = datetime.datetime.combine(current_time.date(), work_calendar.work_start).replace(tzinfo=current_time.tzinfo)
                work_end = datetime.datetime.combine(current_time.date(), work_calendar.work_end).replace(tzinfo=current_time.tzinfo)

                # work_start = datetime.combine(current_time.date(), work_calendar.work_start)
                # work_end = datetime.combine(current_time.date(), work_calendar.work_end)

                if current_time < work_start:
                    current_time = work_start
                elif current_time >= work_end:
                    current_time = day_end + datetime.timedelta(seconds=1)
                else:
                    work_time += min(work_end, end_time) - current_time
                    current_time = min(work_end, end_time)
            else:
                current_time = day_end + datetime.timedelta(seconds=1)

        return work_time
