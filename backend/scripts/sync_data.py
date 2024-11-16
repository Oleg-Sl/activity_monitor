#!/usr/bin/env python

import os
import sys
import asyncio
from pprint import pprint

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from app.bitrix24.clients.bitrix_client import get_bitrix_client
from app.db.db import get_async_session
from app.services.sync_service import SyncService


async def main() -> None:
    db_session = await anext(get_async_session())
    bitrix_client = await get_bitrix_client()
    sync_service = SyncService(db_session, bitrix_client)
    await sync_service.sync_all_data()


if __name__ == "__main__":
    asyncio.run(main())
