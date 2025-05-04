from typing import List, Optional
from pydantic import ValidationError

from app.constants.common import PRODUCTION_ORDER_TYPE_ID
from app.services.bitrix24.bitrix_client import InterfaceBitrixClient
from app.schemas.product_order_schema import ProductOrderInSchema
from app.infrastructure.file_downloader.file_downloader import FileDownloader
from app.services.file_service import FileServiceFactory
from app.repositories.production_schedule_repository import ProductionScheduleRepository
from app.repositories.stage_history_repository import StageHistoryRepository
from app.repositories.work_calendar_repository import WorkCalendarRepository
from app.repositories.stage_repository import StageRepository
from app.models.stage import Stages


class ProductionOrderService:
    def __init__(
        self,
        bitrix_client: InterfaceBitrixClient,
        production_repo: ProductionScheduleRepository,
        history_repo: StageHistoryRepository,
        stage_repo: StageRepository,
        calendar_repo: WorkCalendarRepository,
    ):
        self.bitrix_client = bitrix_client
        self.entity_type_id = PRODUCTION_ORDER_TYPE_ID
        self.file_service = FileServiceFactory.create()

        self.production_repo = production_repo
        self.history_repo = history_repo
        self.stage_repo = stage_repo
        self.calendar_repo = calendar_repo

    async def get_production_orders(self, production_orders_ids: List[int]) -> List[ProductOrderInSchema]:
        if not production_orders_ids:
            return []

        try:
            filter_data = {"@id": list(set(production_orders_ids))}
            raw_production_orders = [production_order async for production_order in self.bitrix_client.get_entities(self.entity_type_id, filter_data)]

            production_orders = []
            errors = []

            for production_order in raw_production_orders:
                try:
                    order = ProductOrderInSchema(**production_order)
                    production_orders.append(order)
                except ValidationError as e:
                    errors.append({"data": production_order, "error": e.errors()})
            return [await self._prepare_product_order_data(production_order) for production_order in production_orders]
        except Exception as e:
            return []
    
    async def _prepare_product_order_data(self, production_order: ProductOrderInSchema) -> ProductOrderInSchema:
        image_url = production_order.image_url
        if image_url:
            image_data = await self.file_service.save_file_from_url(image_url)
            if image_data:
                production_order.image_token = image_data.get('image_token')
                production_order.image_local_path = image_data.get('image_path')

        return production_order

    async def save_orders_to_db(self, production_orders_ids: List[int]):
        production_orders = await self.get_production_orders(production_orders_ids)
        for order in production_orders:
            # print('>>> ', type(order))
            # new_stage = await self.stage_repo.get_by_status_id(order.stage_id_str)
            # print('>>> ', new_stage)
            await self._save_order_and_stage_history(order)

    async def _save_order_and_stage_history(self, order: ProductOrderInSchema):
        # Поиск идентификатора стадии по его текстовому представлению
        new_stage = await self.stage_repo.get_by_status_id(order.stage_id_str)
        new_stage_id = new_stage.id if new_stage else None
        order.stage_id = new_stage_id

        old_order = await self.order_repo.get(order.id)
        old_stage_id = old_order.stage_id if old_order else None

        if old_order:
            new_order_id = await self.order_repo.edit_one(order.id, order.model_dump())
        else:
            new_order_id = await self.order_repo.add_one(order.model_dump())
