from sqlalchemy.ext.asyncio import AsyncSession


# from ..bitrix24.services.stage import BitrixStageSchema
from ..bitrix24.services.stages import StageService
from ..bitrix24.clients.bitrix_interface import InterfaceBitrixClient
from ..models.stages import Stages


class SyncService:
    def __init__(self, db: AsyncSession, client: InterfaceBitrixClient) -> None:
        self.db = db
        self.stage_service = StageService(db, client)
    
    async def sync_all_data(self) -> None:
        await self.sync_stages()

    async def sync_stages(self) -> None:
        stages = self.stage_service.fetch_data()
        async for stage in stages:
            # print(stage)
            instance = Stages(**stage.model_dump())
            self.db.add(instance)
            await self.db.commit()
            # print("instance id = ", instance.id)

    async def smart_process(self) -> None:
        pass

    async def sync_users(self):
        pass
