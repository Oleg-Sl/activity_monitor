print("settings.py loaded")

import logging
from typing import Annotated
from fastapi import APIRouter, Request, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import UOWDep
from app.services.credential_service import CredentialsService
from app.schemas.credentials import CredentialSchema, CredentialsFormSchema, BitrixClientSchema


router = APIRouter(
    prefix="/bitrix",
    tags=["Bitrix"],
)
templates = Jinja2Templates(directory="app/templates")


logging.basicConfig(level=logging.INFO, filename="logs/request/settings.log",
                    format="%(asctime)s %(levelname)s %(message)s")


@router.post("/index", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/install", response_class=HTMLResponse)
async def install(
    request: Request,
    DOMAIN: Annotated[str, Query()],
    data: Annotated[CredentialsFormSchema, Form()],
    uow: UOWDep
) -> HTMLResponse:
    credential_data = CredentialSchema(
        domain=DOMAIN,
        auth_token=data.auth_token,
        refresh_token=data.refresh_token
    )
    credential_id = await CredentialsService().add_credential(uow, credential_data)
    return templates.TemplateResponse(request=request, name="install.html", context={"credential_id": credential_id})
