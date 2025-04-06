import asyncio
from sqlalchemy import event


from app.bitrix24.factory import get_bitrix_client
from app.db.db import async_session_maker
from app.repositories.entity_repository import EntityRepository
from app.repositories.stage_repository import StageRepository
from app.models.entity import Entities, save_stage_history
from app.models.stage import Stages



async def sync_entities_task():
    ENTITY_TYPE_ID = 166

    async with async_session_maker() as session:
        repository = EntityRepository(session)
        stage_repository = StageRepository(session)
        bitrix_client = get_bitrix_client(session)
        filter_data = {
            # ">=createdTime": "",
            # "<=createdTime": "",
            "@id": [3103, ]
        }
        async for entity in bitrix_client.get_entities(ENTITY_TYPE_ID, filter_data):
            print("entity1 = ", entity.model_dump())
            stage = await stage_repository.filter(Stages.status_id == entity.stage_id)

            if stage:
                entity.stage_id = stage.id
                print("entity2 = ", entity.model_dump())
                entity_id = await repository.create_or_update(entity.model_dump())
                # save_stage_history

    #     sync_service = SyncService(session, client)
    #     await update_work_calendar(session, 2025)


if __name__ == "__main__":
    asyncio.run(sync_entities_task())

# python -m app.tasks.sync_entities
# .\venv\Scripts\activate
