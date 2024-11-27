import logging
from typing import Annotated
from fastapi import APIRouter, Request, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field


class BitrixSettingsFormSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    auth_token: str = Field(..., validation_alias='AUTH_ID')
    refresh_token: str = Field(..., validation_alias='REFRESH_ID')


class BitrixSettingsQuerySchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    domain: str = Field(..., validation_alias='DOMAIN')
    refresh_token: str = Field(..., validation_alias='APP_SID')

# from app.schemas.bitrix.settings import BitrixSettingsFormSchema

# from api.dependencies import UOWDep
# from schemas.tasks import TaskSchemaAdd, TaskSchemaEdit
# from services.tasks import TasksService

logging.basicConfig(level=logging.INFO, filename="request.log",
                    format="%(asctime)s %(levelname)s %(message)s")

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/index", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/install", response_class=HTMLResponse)
async def install(request: Request, DOMAIN: Annotated[str, Query()], data: Annotated[BitrixSettingsFormSchema, Form()]) -> HTMLResponse:
    logging.info("install")
    logging.info({
        "DOMAIN": DOMAIN,
        "auth_token": data.auth_token,
        "refresh_token": data.refresh_token
    })
    # logging.info(request.query_params)
    # logging.info(data)
    return templates.TemplateResponse(request=request, name="install.html")


# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="item.html", context={"id": id}
#     )