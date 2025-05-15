from typing import List, AsyncGenerator

from app.services.bitrix24.bitrix_client import InterfaceBitrixClient
from app.constants.common import NUMBER_OF_EVENTS_RETRIEVED, MAX_EVENT_REQUEST


class BitrixEventFetcher:
    def __init__(self, bitrix_client: InterfaceBitrixClient):
        self.bitrix_client = bitrix_client

    # async def fetch_production(self, entity_type_id: str, filter_params: dict) -> AsyncGenerator[List[int], None]:
    #     for _ in range(MAX_EVENT_REQUEST):
    #         entity_ids = await self._fetch_events(event_name, limit_events)
    #         if not entity_ids:
    #             break
    #         yield entity_ids
    #     while True:
    #         try:
    #             events = await self.bitrix_client.get_entities(entity_type_id, filter_params)
    #             return [
    #                 event.get("FIELDS", {}).get("ID")
    #                 for event in events
    #                 if event.get("FIELDS", {}).get("ID")
    #             ]
    #         except Exception as e:
    #             pass


    async def fetch_events(self, event_name: str, limit_events: int = NUMBER_OF_EVENTS_RETRIEVED) -> AsyncGenerator[List[int], None]:
        for _ in range(MAX_EVENT_REQUEST):
            entity_ids = await self._fetch_events(event_name, limit_events)
            if not entity_ids:
                break
            yield entity_ids

    async def _fetch_events(self, event_name: str, limit_events: int, ) -> List[int]:
        try:
            events = await self.bitrix_client.get_offline_events(event_name, limit_events)
            return [
                event.get("FIELDS", {}).get("ID")
                for event in events
                if event.get("FIELDS", {}).get("ID")
            ]
        except Exception as e:
            pass
