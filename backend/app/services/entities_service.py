from typing import List

class BitrixEventClient:
    async def get_entities(self, entity_ids: List[int]) -> List[dict]:
        if not entity_ids:
            return []
        entities = await self.entity_workshop_service.get_entities(entity_ids)
        return entities


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
