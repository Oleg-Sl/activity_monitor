from backend.app.bitrix24.services.stages import sync_stages
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session


async def sync_data():
    db = next(get_async_session())
