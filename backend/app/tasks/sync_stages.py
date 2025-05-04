import asyncio


from app.services.bitrix24.factory import get_bitrix_client
from app.db.session import async_session_maker
from app.repositories.stage_repository import StageRepository


async def sync_stages_task():
    async with async_session_maker() as session:
        repository = StageRepository(session)
        bitrix_client = get_bitrix_client(session)
        async for stage in bitrix_client.get_stages():
            stage_id = await repository.create_or_update(stage.model_dump())


if __name__ == "__main__":
    asyncio.run(sync_stages_task())


# python -m app.tasks.sync_stages
# .\venv\Scripts\activate
