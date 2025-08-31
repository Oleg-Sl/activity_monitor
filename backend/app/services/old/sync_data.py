from sqlalchemy.ext.asyncio import AsyncSession


# from ..bitrix24.services.stage import BitrixStageSchema
from app.bitrix24.service import BitrixService
from app.bitrix24.clients.bitrix_interface import InterfaceBitrixClient
from backend.app.models.stage import Stages


class SyncService:
    def __init__(self, db: AsyncSession, client: InterfaceBitrixClient) -> None:
        self.db = db
        self.bx24_service = BitrixService(client)
    
    async def sync_all_data(self) -> None:
        await self.sync_stages()

    async def sync_stages(self) -> None:
        stages = await self.bx24_service.fetch_stages()
        print("stages = ", stages)
        # async for stage in stages:
        #     instance = Stages(**stage.model_dump())
        #     self.db.add(instance)
        #     await self.db.commit()
        #     # print("instance id = ", instance.id)

    async def smart_process(self) -> None:
        pass

    async def sync_users(self):
        pass
