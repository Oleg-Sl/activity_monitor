import logging
from fastapi import APIRouter, Request, Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


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
async def install(request: Request, data = Body()) -> HTMLResponse:
    logging.info("install")
    logging.info(data)
    logging.info(request.body())
    return templates.TemplateResponse(request=request, name="install.html")


# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="item.html", context={"id": id}
#     )