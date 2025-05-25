# import copy
import datetime
# from typing import List, Optional
# from pydantic import ValidationError
# from sqlalchemy.ext.asyncio import AsyncSession

# # from app.constants.production_order import PRODUCTION_ORDER_TYPE_OF_PRODUCT
# # from app.constants.common import PRODUCTION_ORDER_TYPE_ID
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
# from app.services.workcalendar_service import WorkCaldendarService
from app.repositories.production_history_repository import ProductionHistoryRepository

class ProductionHistoryService:
    def __init__(self, production_history_repo: ProductionHistoryRepository):
        self.production_history_repo = production_history_repo

    def log_production_stage(self, production_order_id: int, stage_id_str: str, moved_time: datetime.datetime):
        self.production_history_repo.add_one({
            'production_order_id': production_order_id,
            'stage_id_str': stage_id_str,
            'moved_time': moved_time
        })


# id: Mapped[int] = mapped_column(primary_key=True)
# production_order_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('production_order.id'))
# stage_id_str: Mapped[str] = mapped_column(String(255), comment="Стадия - абревиатура")
# moved_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Когда передвинут")
