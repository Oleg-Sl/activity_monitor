import time
from typing import List, Optional
from pydantic import ValidationError

# from app.constants.common import PRODUCTION_ORDER_TYPE_ID
from app.constants.production_order import PRODUCTION_ORDER_TYPE_ID

from app.services.bitrix24.bitrix_client import InterfaceBitrixClient
from app.schemas.product_order_schema import ProductOrderInSchema
from app.infrastructure.file_downloader.file_downloader import FileDownloader
from app.services.file_service import FileServiceFactory
from app.repositories.production_order_repository import ProductionOrderRepository
# from app.repositories.stage_history_repository import StageHistoryRepository
from app.repositories.production_history_repository import ProductionHistoryRepository

from app.repositories.work_calendar_repository import WorkCalendarRepository
from app.repositories.stage_repository import StageRepository
from app.models.stage import Stages


class ProductionOrderService:
    def __init__(
        self,
        bitrix_client: InterfaceBitrixClient,
        order_repo: ProductionOrderRepository,
        history_repo: ProductionHistoryRepository,
        stage_repo: StageRepository,
        calendar_repo: WorkCalendarRepository,
    ):
        self.bitrix_client = bitrix_client
        self.entity_type_id = PRODUCTION_ORDER_TYPE_ID
        self.file_service = FileServiceFactory.create()

        self.order_repo = order_repo
        self.history_repo = history_repo
        self.stage_repo = stage_repo
        self.calendar_repo = calendar_repo

    async def sync_production(self, date_start, date_end):
        print(date_start, date_end)
        production_orders = self.filter_production_orders({
            '>=updatedTime': date_start,
            '<=updatedTime': date_end,
        })
        result = []
        async for order in production_orders:
            await self._save_order_and_stage_history(order)

        print(len(result))

    async def save_orders_to_db(self, production_orders_ids: List[int]):
        production_orders = await self.get_production_orders(production_orders_ids)
        for order in production_orders:
            await self._save_order_and_stage_history(order)

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

    async def filter_production_orders(self, filter_data: dict):
        result = []
        try:
            # raw_production_orders = [
            #     production_order
            #     async for production_order in self.bitrix_client.get_entities(self.entity_type_id, filter_data)
            # ]
            errors = []

            # for production_order in raw_production_orders:
            async for production_order in self.bitrix_client.get_entities(self.entity_type_id, filter_data):

                try:
                    order = ProductOrderInSchema(**production_order)
                    production_data = await self._prepare_product_order_data(order)
                    yield production_data
                except ValidationError as e:
                    print(f"Ошибка валидации заказа {production_order.get('id')}: {e}")
                    # Можно добавить логирование ошибок
                    continue
                except Exception as e:
                    print(f"Ошибка обработки заказа {production_order.get('id')}: {e}")
                    continue
                # result.append(production_order)
                # print("result = ", len(result))
                # # yield production_order
                # # print('===> ', production_order)
                # try:
                #     order = ProductOrderInSchema(**production_order)
                #     production_data = await self._prepare_product_order_data(order)
                #     yield production_data
                # except ValidationError as e:
                #     print("err 1 = ", e)
                #     errors.append({"data": production_order, "error": e.errors()})
        except Exception as e:
            print("err 2 = ", e)
            pass

    async def _prepare_product_order_data(self, production_order: ProductOrderInSchema) -> ProductOrderInSchema:
        image_url = production_order.image_url
        if image_url:
            image_data = await self.file_service.save_file_from_url(image_url)
            if image_data:
                production_order.image_token = image_data.get('image_token')
                production_order.image_local_path = image_data.get('image_path')

        return production_order

    async def _save_order_and_stage_history(self, order: ProductOrderInSchema):
        # Поиск идентификатора стадии по его текстовому представлению
        new_stage = await self.stage_repo.get_by_status_id(order.stage_id_str)
        new_stage_id = new_stage.id if new_stage else None
        order.stage_id = new_stage_id

        old_order = await self.order_repo.get(order.id)
        old_stage_id = old_order.stage_id if old_order else None

        if old_order:
            order_id = await self.order_repo.edit_one(order.id, order.model_dump())
        else:
            order_id = await self.order_repo.add_one(order.model_dump())

        print(order.id)
        print('order_id = ', order_id)
        # print('stage_id: ', old_stage_id if old_stage_id else '-', ' -> ', new_stage_id)
        print('stage_id: ', old_order.stage_id_str if old_order else '-', ' -> ', order.stage_id_str)

        # self.order_repo.commit()

        # result = await self.history_repo.log_stage_change(
        #     order.entity_type_id,
        #     order.product_id,
        #     None,
        #     old_stage_id,
        #     new_stage_id,
        #     order.moved_time
        # )

        # # Сохраняем/обновляем заказ
        # saved_order = await self.order_repo.save_or_update(order)
        # # Извлекаем время изменения стадии
        # stage_changed_at = order.stage_changed_at
        # now = datetime.now()
        # # Получаем продолжительность на стадии
        # working_hours = await self.calendar_repo.calculate_working_hours(stage_changed_at, now)
        # # Сохраняем в историю стадий
        # await self.history_repo.save_stage_change(
        #     order_id=saved_order.id,
        #     stage=order.stage,
        #     started_at=stage_changed_at,
        #     duration=working_hours
        # )





























    # async def update_entity(self, entity: WorkOrderSchema) -> WorkOrderSchema:
    #     image_data = await self.uploads_image(entity.image_url)
    #     if image_data:
    #         entity.image_token = image_data.get('image_token')
    #         entity.image_local_path = image_data.get('image_path')
    #     return entity

    # async def uploads_image(self, url: str, old_image_token: Optional[str] = None) -> dict:
    #     relative_path = await self.file_service.save_file_from_url(
    #         url=url,
    #         old_image_token=old_image_token,
    #         # filename='test_file'
    #     )
    #     return relative_path
