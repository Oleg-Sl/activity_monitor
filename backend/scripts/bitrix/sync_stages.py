#!/usr/bin/env python

import os
import sys
import asyncio
from pprint import pprint

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from app.bitrix24.bitrix_webhook import BitrixWebhook
from app.schemas.bitrix.stages import BitrixStageSchema


async def sync_stages(entity_id):
    api = BitrixWebhook()
    result = await api.call("crm.status.list", {
        "filter": {
            # "ENTITY_ID": "DYNAMIC_166_STAGE_29"
            "ENTITY_ID": entity_id
        },
        "order": {
            "ID": "DESC"
        },
    })
    pprint(result)
    # for stage in result["result"]:
    #     stage_data = BitrixStageSchema(**stage)
    #     pprint(stage_data.model_dump())



if __name__ == "__main__":
    asyncio.run(main())
