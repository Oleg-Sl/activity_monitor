from typing import List, Optional
from pydantic import ValidationError
from pprint import pprint

from app.constants.product_schedule import PRODUCTION_SCHEDULE_TYPE_ID

from app.services.bitrix24.bitrix_client import InterfaceBitrixClient
# from app.schemas.product_order_schema import ProductOrderInSchema
from app.schemas.product_schedule_schema import ProductScheduleInSchema
# from app.infrastructure.file_downloader.file_downloader import FileDownloader
from app.services.file_service import FileServiceFactory
# from app.repositories.production_schedule_repository import ProductionScheduleRepository
from app.repositories.production_order_repository import ProductionOrderRepository
# from app.repositories.stage_history_repository import StageHistoryRepository
from app.repositories.production_history_repository import ProductionHistoryRepository

from app.repositories.work_calendar_repository import WorkCalendarRepository
from app.repositories.stage_repository import StageRepository
# from app.models.stage import Stages


class ProductionScheduleService:
    def __init__(
        self,
        bitrix_client: InterfaceBitrixClient,
        production_repo: ProductionOrderRepository,
        history_repo: ProductionHistoryRepository,
        stage_repo: StageRepository,
        calendar_repo: WorkCalendarRepository,
    ):
        self.bitrix_client = bitrix_client
        self.entity_type_id = PRODUCTION_SCHEDULE_TYPE_ID
        self.file_service = FileServiceFactory.create()

        self.production_repo = production_repo
        self.history_repo = history_repo
        self.stage_repo = stage_repo
        self.calendar_repo = calendar_repo

    async def get_production(self, production_ids: List[int]) -> List[ProductScheduleInSchema]:
        if not production_ids:
            return []

        try:
            filter_data = {"@id": list(set(production_ids))}
            raw_productions = [production async for production in self.bitrix_client.get_entities(self.entity_type_id, filter_data)]
            productions = []
            errors = []

            for production in raw_productions:
                try:
                    # print('ufCrm9_1737034529 = ', production['ufCrm9_1737034529'])
                    order = ProductScheduleInSchema(**production)
                    productions.append(order)
                except ValidationError as e:
                    pprint('Error: ', e)
                    pprint(production)
                    errors.append({"data": production, "error": e.errors()})
            if errors:
                print('Errors in receiving production of schedule: ', errors)
            return productions
            # return [await self._prepare_product_order_data(production) for production in productions]
        except Exception as e:
            print(e)
            return []

    async def filter_production_orders(self, filter_data: dict):
        try:
            raw_productions = [production async for production in self.bitrix_client.get_entities(self.entity_type_id, filter_data)]
            errors = []

            for raw_production in raw_productions:
                # print('===> ', raw_production)
                try:
                    # print('ufCrm9_1737034529 = ', raw_production['ufCrm9_1737034529'])
                    production = ProductScheduleInSchema(**raw_production)
                    yield production
                except ValidationError as e:
                    pprint(e)
                    print(raw_production)
                    errors.append({"data": raw_production, "error": e.errors()})
        except Exception as e:
            pass


    async def sync_production(self, date_start, date_end):
        productions = self.filter_production_orders({
            '>=updatedTime': date_start,
            '<=updatedTime': date_end,
        })
        async for production in productions:
            await self._save_production_and_stage_history(production)

    # async def _prepare_product_order_data(self, production_order: ProductScheduleInSchema) -> ProductScheduleInSchema:
    #     image_url = production_order.image_url
    #     if image_url:
    #         image_data = await self.file_service.save_file_from_url(image_url)
    #         if image_data:
    #             production_order.image_token = image_data.get('image_token')
    #             production_order.image_local_path = image_data.get('image_path')
    #     return production_order

    async def save_productions_to_db(self, production_ids: List[int]):
        productions = await self.get_production(production_ids)
        for production in productions:
            # print('production = ', production)
            await self._save_production_and_stage_history(production)

    async def _save_production_and_stage_history(self, production: ProductScheduleInSchema):
        # print('production.id = ', production.id)

        # Поиск идентификатора стадии по его текстовому представлению
        new_stage = await self.stage_repo.get_by_status_id(production.stage_id_str)
        new_stage_id = new_stage.id if new_stage else None
        production.stage_id = new_stage_id

        old_order = await self.production_repo.get(production.id)
        old_stage_id = old_order.stage_id if old_order else None
        # print('old_order = ', old_order)

    
        # print('old_order = ', old_order)
        if old_order:
            new_order_id = await self.production_repo.edit_one(production.id, production.model_dump())
        else:
            new_order_id = await self.production_repo.add_one(production.model_dump())

        # self.history_repo.add_one({
        #     'production_order_id': production_order_id,
        #     'stage_id_str': stage_id_str,
        #     'moved_time': moved_time
        # })

        # print({
        #     'production_order_id': new_order_id,
        #     'stage_id_str': old_order.stage_id_str,
        #     # 'stage_id_str': production.stage_id_str,
        #     'moved_time': production.moved_time
        # })
        if old_stage_id != new_stage_id:
            res = await self.history_repo.add_one({
                'production_order_id': new_order_id,
                'stage_id_str': old_order.stage_id_str,
                # 'stage_id_str': production.stage_id_str,
                'moved_time': production.moved_time
            })

        print('new_order_id = ', new_order_id)
        print('res = ', res)
