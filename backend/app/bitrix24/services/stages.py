import os
import sys
import asyncio
from pprint import pprint
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

from ..clients.bitrix_webhook import BitrixWebhook
from app.schemas.bitrix.stages import BitrixStageSchema
from ..clients.bitrix_interface import InterfaceBitrixClient


class StageService:
    def __init__(self, db: AsyncSession, client: InterfaceBitrixClient) -> None:
        self.db = db
        self.client = client

    async def fetch_data(self, entity_id: str = None) -> AsyncGenerator[BitrixStageSchema]:
        filter_data = { "ENTITY_ID": entity_id } if entity_id else {}
        result = await self.client.call("crm.status.list", {
            "filter": filter_data
        })

        for stage in result.get("result", []):
            # pprint(stage)
            yield BitrixStageSchema(**stage)
        


# async def sync_stages(entity_id, ):
#     api = BitrixWebhook()
#     result = await api.call("crm.status.list", {
#         "filter": {
#             "ENTITY_ID": entity_id
#         },
#         "order": {
#             "ID": "DESC"
#         },
#     })
#     pprint(result)
#     for stage in result.get("result", []):
#         stage_data = BitrixStageSchema(**stage)

#         # pprint(stage_data.model_dump())


