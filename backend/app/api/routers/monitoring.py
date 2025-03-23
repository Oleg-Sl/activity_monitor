print("settings.py loaded")

import logging
from typing import Annotated
from fastapi import APIRouter, Request, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import UOWDep
from app.services.credentials import CredentialsService
from app.schemas.credentials import BitrixClientSchema


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
