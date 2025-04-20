print("settings.py loaded")

import logging
from datetime import datetime, timezone
from typing import Annotated, Dict
from fastapi import APIRouter, Request, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import UOWDep
from app.services.credentials import CredentialsService
from app.schemas.credentials import BitrixClientSchema
from app.db.db import async_session_maker
from app.repositories.entity_repository import EntityRepository
from app.repositories.stage_repository import StageRepository
from app.models.stage import Stages
from app.models.entity import Entities
from app.parameters.params import KANBAN_ITEMS


router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"],
)


logging.basicConfig(level=logging.INFO, filename="request/monitoring.log",
                    format="%(asctime)s %(levelname)s %(message)s")



@router.post("/client-data")
async def client_data(
    data: BitrixClientSchema,
    uow: UOWDep
):
    credentials = await CredentialsService().get_credentials(uow)
    if credentials:
        await CredentialsService().edit_credential(uow, credentials[-1].id, data)

    return {"OK": True}


@router.post("/entities")
async def get_entities(
    uow: UOWDep
):
    async with async_session_maker() as session:
        repository = EntityRepository(session)
        data = await repository.get_grouped_by_kanban()
        return data
    # async with async_session_maker() as session:
    #     repository = EntityRepository(session)
    #     stage_repository = StageRepository(session)

    #     all_status_ids = sum((v['status_id'] for v in KANBAN_ITEMS.values()), [])

    #     # Получаем все entities по этим стадиям
    #     entities = await repository.filter(Entities.stage_id_str.in_(all_status_ids))

    #     result: Dict[str, list] = {key: [] for key in KANBAN_ITEMS}

    #     now = datetime.now(timezone.utc)
        
    #     # stages = await stage_repository.filter(Stages.status_id.in_(['DT166_31:UC_HNUB5Y', 'DT166_31:CLIENT']))
    #     # stage_ids = [stage.id for stage in stages]
    #     # entities = await repository.filter(Entities.stage_id_str.in_(['DT166_31:UC_HNUB5Y', 'DT166_31:CLIENT', 'DT166_29:NEW']))
    #     # print('+'*88)
    #     # print('entities = ', entities)
    #     for entity in entities:
    #         current_group = None
    #         for group_key, group_data in KANBAN_ITEMS.items():
    #             if entity.stage_id_str in group_data['status_id']:
    #                 current_group = group_key
    #                 break

    #         if current_group is None:
    #             continue  # стадия не входит ни в одну из групп

    #         # Ищем стадию без end_time
    #         stmt = select(StageHistory).where(
    #             StageHistory.entity_id == entity.id,
    #             StageHistory.end_time.is_(None)
    #         )
    #         stage_result = await session.execute(stmt)
    #         current_stage = stage_result.scalars().first()

    #         total_time = None
    #         if current_stage:
    #             total_time = now - current_stage.start_time

    #         result[current_group].append({
    #             "id": entity.id,
    #             "title": entity.title,
    #             "stage_id": entity.stage_id,
    #             "stage_str": entity.stage_id_str,
    #             "stage_duration_seconds": total_time.total_seconds() if total_time else None,
    #             "stage_duration_human": str(total_time) if total_time else None,
    #             "created_time": entity.created_time.isoformat(),
    #             "updated_time": entity.updated_time.isoformat(),
    #         })


    # return result



