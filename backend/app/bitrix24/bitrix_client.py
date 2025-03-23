from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from pydantic import BaseModel, ValidationError
from typing import List, Optional

from app.schemas.stage import StageSchema
from app.schemas.entity import EntitySchema


class InterfaceBitrixClient(ABC):
    @abstractmethod
    async def call(self, method: str, data: dict, count: int = None) -> dict:
        raise NotImplementedError
    
    @abstractmethod
    async def batch(self, data: dict) -> dict:
        raise NotImplementedError

    async def get_stages(self, entity_id: str = None) -> AsyncGenerator[StageSchema, None]:
        filter_data = { "ENTITY_ID": entity_id } if entity_id else {}
        response = await self.call("crm.status.list", {
            "filter": filter_data
        })

        for stage in response.get("result", []):
            try:
                yield StageSchema(**stage)
            except ValidationError as e:
                print(f"Ошибка валидации данных: {e}")
                continue

    async def get_entities(self, entityTypeId: str, filter_params: Optional[dict] = None) -> AsyncGenerator[EntitySchema, None]:
        if filter_params is None:
            filter_params = {}

        entity_id = 0
        while True:
            filter_params[">id"] = entity_id
            response = await self.call("crm.item.list", {
                "entityTypeId": entityTypeId,
                "filter": filter_params,
                "order": {
                    "id": "ASC"
                }
            })

            entities = response.get("result", {}).get("items", [])
            if not entities:
                break

            for entity in entities:
                try:
                    yield EntitySchema(**entity)
                except ValidationError as e:
                    print(f"Ошибка валидации данных: {e}")
                    continue

            entity_id = entities[-1]["id"]
    
    async def get_entities_by_ids(self, entityTypeId: str, entity_ids: list[int]):
        cmd = {
            entity_id: f"crm.item.list?entityTypeId={entityTypeId}&filter[id]={entity_id}"
            for entity_id in entity_ids
        }

        response = await self.call("batch", {
            "halt": 0,
            "cmd": cmd
        })

        result = response.get("result", {}).get("result", {})
        for res_command in result.values():
            for entity_list in res_command.values():
                for entity in entity_list:
                    try:
                        yield EntitySchema(**entity)
                    except ValidationError as e:
                        print(f"Ошибка валидации данных: {e}")
                        continue

    async def get_offline_events(self, event_name: str, limit: Optional[int] = 50) -> list[int]:
        response = await self.call("event.offline.get", {
            "filter": {
                "EVENT_NAME": event_name
            },
            "order": {"TIMESTAMP_X": "ASC"},
            "limit": limit
        })

        if "error" in response:
            print(response.get("error"))
            print(response.get("error_description"))

        events = response.get("result", {}).get("events", [])

        return [
            event["EVENT_DATA"]
            for event in events
            if event.get("EVENT_DATA")
        ]
