print("settings.py loaded")

import logging
from datetime import datetime, timezone
from typing import Annotated, Dict
from fastapi import APIRouter, Request, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import UOWDep
# from app.services.credentials import CredentialsService
from app.schemas.credentials import BitrixClientSchema
from app.db.session import async_session_maker
# from app.repositories.entity_repository import EntityRepository
# from app.repositories.workorder_repository import WorkOrderRepository
from app.repositories.stage_repository import StageRepository
from app.models.stage import Stages
# from app.models.entity import Entities
# from app.parameters.params import KANBAN_ITEMS
from app.services.production_service import ProductionService
from app.services.workcalendar_service import WorkCaldendarService

from app.repositories.production_order_repository import ProductionOrderRepository
from app.repositories.work_calendar_repository import WorkCalendarRepository
from app.repositories.production_schedule_repository import ProductionScheduleRepository
from app.constants.kanban import SAWING_AND_ASSEMBLY_ITEMS, SAWING_AND_ASSEMBLY_KANBAN


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


@router.post("/sawing")
async def get_sawing():
    async with async_session_maker() as session:
        production_order_repository = ProductionOrderRepository(session)
        work_calendar_repository = WorkCalendarRepository(session)
        work_calendar_service = WorkCaldendarService(work_calendar_repository)
        service = ProductionService(production_order_repository, work_calendar_service)
        return await service.get_kanban_data(SAWING_AND_ASSEMBLY_KANBAN)
        # return await service.get_orders_grouped_by_stage(SAWING_AND_ASSEMBLY_ITEMS)
