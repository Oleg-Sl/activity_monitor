import os
import logging
import asyncio
import pprint
from typing import List, Any, Optional
from collections import defaultdict
from logging.handlers import TimedRotatingFileHandler
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.bitrix24.factory import get_bitrix_client
from app.bitrix24.bitrix_client import InterfaceBitrixClient
from app.db.db import async_session_maker
# from app.schemas.entity import EntitySchema
from app.schemas.work_order import WorkOrderSchema
# from app.repositories.entity_repository import EntityRepository
from app.repositories.workorder_repository import WorkOrderRepository
from app.models.work_order import WorkOrder, save_stage_history
from app.parameters.params import WORKSHOP_TYPE_OF_PRODUCT, PRODUCT_TYPE_DATA, ALLOCATED_HOURS, ZAKUP_FIELDS
from app.services.file_service import FileServiceFactory


# Создание директории logs, если её нет
os.makedirs("logs", exist_ok=True)

file_handler = TimedRotatingFileHandler(
    filename="logs/sync_entities.log",
    when="midnight",              # Ротация каждый день в полночь
    interval=1,                   # Каждые 1 сутки
    backupCount=7,                # Хранить 7 файлов
    encoding="utf-8",             # Поддержка кириллицы
    utc=True                      # Использовать UTC, можно убрать если хочешь локальное время
)
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


WORKORDER_TYPE_ID = 166    # ID смартпроцесса производство
FOT_TYPE_ID = 1048      # ID смартпроцесса производство
ZAKUP_TYPE_ID = 128     # ID смартпроцесса закуп

LIMIT_EVENTS = 25       # кол-во событий извлекаемых из очереди за один запрос
REQUESTS_COUNT = 5      # кол-во запросов данных выполняемых в одной задаче
TIMEOUT = 1             # пауза между выполняемыми запросами (сек.)


class WorkorderService:
    def __init__(self, bitrix_client: InterfaceBitrixClient):
        self.bitrix_client = bitrix_client
        self.file_service = FileServiceFactory.create()
        self.entity_type = WORKORDER_TYPE_ID

    async def get_entities(self, entity_ids: list[int]) -> list[WorkOrderSchema]:
        if not entity_ids:
            return []
        try:
            filter_data = {"@id": list(set(entity_ids))}
            raw_entities = [entity async for entity in self.bitrix_client.get_entities(self.entity_type, filter_data)]
            entities = [WorkOrderSchema(**entity) for entity in raw_entities]
            return [await self.update_entity(entity) for entity in entities]
        except Exception as e:
            logger.exception("Failed to fetch workshop entities: %s", e)
            return []
    
    async def update_entity(self, entity: WorkOrderSchema) -> WorkOrderSchema:
        image_data = await self.uploads_image(entity.image_url)
        if image_data:
            entity.image_token = image_data.get('image_token')
            entity.image_local_path = image_data.get('image_path')
        return entity

    async def uploads_image(self, url: str, old_image_token: Optional[str] = None) -> dict:
        relative_path = await self.file_service.save_file_from_url(
            url=url,
            old_image_token=old_image_token,
            # filename='test_file'
        )
        return relative_path


class BitrixEntityEventFetcher:
    def __init__(self, bitrix_client: InterfaceBitrixClient):
        self.bitrix_client = bitrix_client
        self.entity_workshop_service = WorkorderService(bitrix_client)

    async def fetch_events(self, event_name: str, limit_events: int) -> List[WorkOrderSchema]:
        try:
            events = await self.bitrix_client.get_offline_events(event_name, limit_events)
            entity_ids = [event.get("FIELDS", {}).get("ID") for event in events if event.get("FIELDS", {}).get("ID")]
            return await self.fetch_data(entity_ids)
        except Exception as e:
            logger.exception("Failed to fetch events: %s", e)
            return []

    async def fetch_data(self, entity_ids: list[int]) -> List[WorkOrderSchema]:
        if not entity_ids:
            return []
        entities = await self.entity_workshop_service.get_entities(entity_ids)
        return entities


class WorkOrderSaver:
    def __init__(self, work_order_repository: WorkOrderRepository, event_service: BitrixEntityEventFetcher):
        self.work_order_repository = work_order_repository
        self.event_service = event_service
        self.limit_events = LIMIT_EVENTS

    async def save_entities(self, event_name: str):
        cnt = REQUESTS_COUNT

        while cnt > 0:
            work_orders = await self.event_service.fetch_events(event_name, self.limit_events)
            if not work_orders:
                break

            for work_order in work_orders:
                await self.work_order_repository.create_or_update(work_order.model_dump(exclude={'image_url'}))

            cnt -= 1
            if len(work_orders) < self.limit_events:
                break

            await asyncio.sleep(TIMEOUT)
            break


# получение данных из очереди событий
async def event_workorder_task():
    async with async_session_maker() as session:
        bitrix_client = get_bitrix_client(session)
        work_order_repository = WorkOrderRepository(session)
        event_fetcher = BitrixEntityEventFetcher(bitrix_client)
        event_saver = WorkOrderSaver(work_order_repository, event_fetcher)

        await event_saver.save_entities('ONCRMDYNAMICITEMADD_166')
        await event_saver.save_entities('ONCRMDYNAMICITEMUPDATE_166')

        # entities = await event_fetcher.fetch_data([3497, 3269, 3453, 3455, 2833])
        # for entity in entities:
        #     pprint.pprint(entity)


if __name__ == "__main__":
    asyncio.run(event_workorder_task())


# python -m app.tasks.event_workorder
# .\venv\Scripts\activate
