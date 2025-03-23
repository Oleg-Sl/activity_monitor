from abc import ABC, abstractmethod


class InterfaceBitrixClient(ABC):
    @abstractmethod
    async def call(self, method: str, data: dict, count: int = None) -> dict:
        raise NotImplementedError
    
    @abstractmethod
    async def batch(self, data: dict) -> dict:
        raise NotImplementedError


class BitrixClient(InterfaceBitrixClient):
    async def fetch_data(self, entity_id: str = None) -> AsyncGenerator[BitrixStageSchema]:
        
        filter_data = { "ENTITY_ID": entity_id } if entity_id else {}
        result = await self.client.call("crm.status.list", {
            "filter": filter_data
        })

        for stage in result.get("result", []):
            yield BitrixStageSchema(**stage)
        
