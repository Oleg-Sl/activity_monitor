import asyncio

from app.bitrix24.factory import get_bitrix_client
from app.bitrix24.bitrix_client import InterfaceBitrixClient
from app.db.db import async_session_maker
from app.schemas.entity import EntitySchema
from app.repositories.entity_repository import EntityRepository


ENTITY_TYPE_ID = 166    # ID смартпроцесса производство
LIMIT_EVENTS = 25       # кол-во событий извлекаемых из очереди за один запрос
REQUESTS_COUNT = 5      # кол-во запросов данных выполняемых в одной задаче
TIMEOUT = 1             # пауза между выполняемыми запросами (сек.)


class BitrixEntityEventFetcher:
    def __init__(self, bitrix_client: InterfaceBitrixClient):
        self.bitrix_client = bitrix_client

    async def fetch_events(self, event_name: str, limit_events: int) -> list[EntitySchema]:
        events = self.bitrix_client.get_offline_events(event_name, limit_events)
        entity_ids = [event.get("FIELDS", {}).get("ID") for event in events if event.get("FIELDS", {}).get("ID")]

        if not entity_ids:
            return []

        filter_data = {"@id": entity_ids}
        return [entity async for entity in self.bitrix_client.get_entities(ENTITY_TYPE_ID, filter_data)]


class EntitySaver:
    def __init__(self, entity_repository: EntityRepository, event_service: BitrixEntityEventFetcher):
        self.entity_repository = entity_repository
        self.event_service = event_service
        self.limit_events = LIMIT_EVENTS

    async def save_entities(self, event_name: str):        
        cnt = REQUESTS_COUNT

        while cnt > 0:
            entities = await self.event_service.fetch_events(event_name, self.limit_events)
            if not entities:
                break

            for entity in entities:
                self.entity_repository.create_or_update(entity)

            cnt -= 1
            if len(entities) < self.limit_events:
                break

            await asyncio.sleep(TIMEOUT)


# получение данных из очереди событий
async def event_entities_task():
    async with async_session_maker() as session:
        bitrix_client = get_bitrix_client(session)
        entity_repository = EntityRepository(session)
        event_fetcher = BitrixEntityEventFetcher(bitrix_client)
        event_saver = EntitySaver(entity_repository, event_fetcher)

        await event_saver.save_entities('ONCRMDYNAMICITEMADD')
        await event_saver.save_entities('ONCRMDYNAMICITEMUPDATE')


if __name__ == "__main__":
    asyncio.run(event_entities_task())


# python -m app.tasks.sync_entities
# .\venv\Scripts\activate
