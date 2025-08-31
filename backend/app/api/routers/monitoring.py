print("settings.py loaded")

import logging
from fastapi import APIRouter

from app.constants.kanban import SAWING_AND_ASSEMBLY_KANBAN
from app.api.dependencies import UOWDep
from app.schemas.credentials import BitrixClientSchema
from app.db.session import async_session_maker
from app.schemas.kanban_item import KanbanItemSchema
from app.repositories.production_order_repository import ProductionOrderRepository
from app.repositories.work_calendar_repository import WorkCalendarRepository
from app.services.production_service import ProductionService
from app.services.workcalendar_service import WorkCaldendarService
from app.services.credential_service import CredentialsService


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

        # res = [KanbanItemSchema(**stage_kanban) for stage_kanban in SAWING_AND_ASSEMBLY_KANBAN]
        # print(res)
        # return res
        return await service.get_kanban_data(
            [KanbanItemSchema(**stage_kanban) for stage_kanban in SAWING_AND_ASSEMBLY_KANBAN]
        )
