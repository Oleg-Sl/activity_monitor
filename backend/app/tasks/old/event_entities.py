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
from backend.app.db.session import async_session_maker
from app.schemas.entity import EntitySchema
from app.repositories.entity_repository import EntityRepository
from app.parameters.params import WORKSHOP_TYPE_OF_PRODUCT, PRODUCT_TYPE_DATA, ALLOCATED_HOURS, ZAKUP_FIELDS


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

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
#     handlers=[
#         logging.FileHandler("logs/sync_entities.log", encoding="utf-8"),
#         logging.StreamHandler()
#     ]
# )

# logger = logging.getLogger(__name__)


ENTITY_TYPE_ID = 166    # ID смартпроцесса производство
FOT_TYPE_ID = 1048      # ID смартпроцесса производство
ZAKUP_TYPE_ID = 128     # ID смартпроцесса закуп

LIMIT_EVENTS = 25       # кол-во событий извлекаемых из очереди за один запрос
REQUESTS_COUNT = 5      # кол-во запросов данных выполняемых в одной задаче
TIMEOUT = 1             # пауза между выполняемыми запросами (сек.)


class ProductSchema(BaseModel):
    product_id: str
    product_type_str: str
    fot_id: Optional[int] = None
    image: Optional[str] = None


class EntityWorkshopService:
    def __init__(self, bitrix_client: InterfaceBitrixClient):
        self.bitrix_client = bitrix_client
        self.entity_type = ENTITY_TYPE_ID

    async def get_entities(self, entity_ids: list[int]) -> list[EntitySchema]:
        if not entity_ids:
            return []
        try:
            filter_data = {"@id": list(set(entity_ids))}
            raw_entities = [entity async for entity in self.bitrix_client.get_entities(self.entity_type, filter_data)]
            entities = [EntitySchema(**entity) for entity in raw_entities]
            return self.fill_fields(entities)
        except Exception as e:
            logger.exception("Failed to fetch workshop entities: %s", e)
            return []

    def fill_fields(self, entities: list[EntitySchema]) -> list[EntitySchema]:
        for entity in entities:
            try:
                if entity.product_type:
                    meta = WORKSHOP_TYPE_OF_PRODUCT[entity.product_type]
                    entity.name = meta['name']
                    entity.product_type_str = meta['product_type']
            except Exception as e:
                logger.warning("Failed to enrich entity %s: %s", entity.id, e)
        return entities


class EntityProductService:
    def __init__(self, bitrix_client: InterfaceBitrixClient):
        self.bitrix_client = bitrix_client

    async def update_entities(self, entities: list[EntitySchema]) -> list[EntitySchema]:
        if not entities:
            return []
        try:
            products_result = await self.get_products(entities)
            products = self.parse_products(products_result)
            for entity in entities:
                prod = products.get(entity.product_type_str, {}).get(str(entity.product_id))
                if prod:
                    entity.image = prod.image
                    entity.fot_id = prod.fot_id
            return entities
        except Exception as e:
            logger.exception("Failed to update product info for entities: %s", e)
            return entities

    async def get_products(self, entities: list[EntitySchema]) -> dict:
        cmd = {}
        for entity in entities:
            try:
                if not entity.product_id or not entity.product_type:
                    continue
                meta = WORKSHOP_TYPE_OF_PRODUCT[entity.product_type]
                if not meta['is_product']:
                    continue
                fields = meta['fields']
                product_type = meta['product_type']
                cmd[f'{product_type}_{entity.product_id}'] = (
                    f'crm.item.list?entityTypeId={meta["entity_type_id"]}'
                    f'&filter[id]={entity.product_id}'
                    f'&select[]=entityTypeId&select[]=id&select[]={fields["image"]}'
                    f'&select[]={fields["fot_id"]}'
                )
            except Exception as e:
                logger.warning("Invalid entity for product batch: %s", e)

        response = await self.bitrix_client.batch({'halt': 0, 'cmd': cmd})
        return response.get('result', {}).get('result', {})

    def parse_products(self, products: dict) -> dict[str, dict[str, ProductSchema]]:
        result = defaultdict(dict)
        for key, items in products.items():
            try:
                if not items or not items['items']:
                    continue
                product_type_str, product_id = key.split('_')
                product_meta = PRODUCT_TYPE_DATA[product_type_str]
                product_data = items['items'][0]
                print(product_data)
                image = product_data.get(product_meta['fields']['image'], {}).get('urlMachine')
                fot_id = product_data.get(product_meta['fields']['fot_id'])
                result[product_type_str][product_id] = ProductSchema(
                    product_id=product_id,
                    product_type_str=product_type_str,
                    fot_id=fot_id,
                    image=image
                )
            except Exception as e:
                logger.warning("Failed to parse product: %s", e)
        return result
    

class EntityFotService:
    def __init__(self, bitrix_client: InterfaceBitrixClient):
        self.bitrix_client = bitrix_client
        self.entity_type = FOT_TYPE_ID

    async def update_entities(self, entities: list[EntitySchema]) -> list[EntitySchema]:
        fot_ids = [entity.fot_id for entity in entities if entity.fot_id]
        if not fot_ids:
            return entities
        
        try:
            filter_data = {"@id": list(set(fot_ids))}
            fots_raw = [fot async for fot in self.bitrix_client.get_entities(self.entity_type, filter_data)]
            fots = {str(fot['id']): fot for fot in fots_raw}
            for entity in entities:
                try:
                    fot = fots.get(str(entity.fot_id))
                    if not fot:
                        continue
                    for alias, field in ALLOCATED_HOURS.items():
                        setattr(entity, f"allocated_hours_{alias}", fot.get(field))
                except Exception as e:
                    logger.warning("Failed to enrich entity %s with fot: %s", entity.id, e)
        except Exception as e:
            logger.exception("Failed to fetch FOT data: %s", e)
        return entities


class EntityZakupService:
    def __init__(self, bitrix_client: InterfaceBitrixClient):
        self.bitrix_client = bitrix_client
        self.entity_type = ZAKUP_TYPE_ID

    async def update_entities(self, entities: list[EntitySchema]) -> list[EntitySchema]:
        zakup_ids = [entity.zakup_id for entity in entities if entity.zakup_id]
        if not zakup_ids:
            return entities
        try:
            filter_data = {"@id": list(set(zakup_ids))}
            zakups_raw = [zakup async for zakup in self.bitrix_client.get_entities(self.entity_type, filter_data)]
            zakups = {str(zakup['id']): zakup for zakup in zakups_raw}
            # print(zakups_raw)
            for entity in entities:
                try:
                    zakup = zakups.get(str(entity.zakup_id))
                    if not zakup:
                        continue
                    for alias, field in ZAKUP_FIELDS.items():
                        setattr(entity, alias, zakup.get(field))
                except Exception as e:
                    logger.warning("Failed to enrich entity %s with zakup: %s", entity.id, e)
        except Exception as e:
            logger.exception("Failed to fetch zakup data: %s", e)
        return entities


class BitrixEntityEventFetcher:
    def __init__(self, bitrix_client: InterfaceBitrixClient):
        self.bitrix_client = bitrix_client
        self.entity_workshop_service = EntityWorkshopService(bitrix_client)
        self.entity_product_service = EntityProductService(bitrix_client)
        self.entity_fot_service = EntityFotService(bitrix_client)
        self.entity_zakup_service = EntityZakupService(bitrix_client)

    async def fetch_events(self, event_name: str, limit_events: int) -> List[EntitySchema]:
        try:
            events = await self.bitrix_client.get_offline_events(event_name, limit_events)
            entity_ids = [event.get("FIELDS", {}).get("ID") for event in events if event.get("FIELDS", {}).get("ID")]
            return await self.fetch_data(entity_ids)
        except Exception as e:
            logger.exception("Failed to fetch events: %s", e)
            return []

    async def fetch_data(self, entity_ids: list[int]) -> List[EntitySchema]:
        if not entity_ids:
            return []
        entities = await self.entity_workshop_service.get_entities(entity_ids)
        entities = await self.entity_product_service.update_entities(entities)
        entities = await self.entity_fot_service.update_entities(entities)
        entities = await self.entity_zakup_service.update_entities(entities)
        return entities


class EntitySaver:
    def __init__(self, entity_repository: EntityRepository, event_service: BitrixEntityEventFetcher):
        self.entity_repository = entity_repository
        self.event_service = event_service
        self.limit_events = LIMIT_EVENTS

    async def save_entities(self, event_name: str):        
        cnt = REQUESTS_COUNT

        while cnt > 0:
            entities = await self.event_service.fetch_events(event_name, self.limit_events)
            # logger.info(entities)
            print('>>> entities = ', entities)
            if not entities:
                break

            for entity in entities:
                await self.entity_repository.create_or_update(entity.model_dump())

            cnt -= 1
            if len(entities) < self.limit_events:
                break

            await asyncio.sleep(TIMEOUT)
            break


# получение данных из очереди событий
async def event_entities_task():
    async with async_session_maker() as session:
        bitrix_client = get_bitrix_client(session)
        entity_repository = EntityRepository(session)
        event_fetcher = BitrixEntityEventFetcher(bitrix_client)
        event_saver = EntitySaver(entity_repository, event_fetcher)

        # await event_saver.save_entities('ONCRMDYNAMICITEMADD_166')
        # await event_saver.save_entities('ONCRMDYNAMICITEMUPDATE_166')

        entities = await event_fetcher.fetch_data([3269, 3453, 3455, 2833])
        # for entity in entities:
        #     print(entity)


if __name__ == "__main__":
    asyncio.run(event_entities_task())


# python -m app.tasks.event_entities
# .\venv\Scripts\activate
