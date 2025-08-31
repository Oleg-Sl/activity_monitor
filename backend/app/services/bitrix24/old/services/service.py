from collections.abc import AsyncGenerator

from app.bitrix24.clients.bitrix_interface import InterfaceBitrixClient
from app.schemas.bitrix.stages import BitrixStageSchema


class BitrixService:
    def __init__(self, client: InterfaceBitrixClient):
        self.client = client

    async def fetch_stages(self) -> AsyncGenerator[BitrixStageSchema]:
        result = await self.client.call("crm.status.list", {})
        for stage in result.get("result", []):
            yield BitrixStageSchema(**stage)
