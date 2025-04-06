print("settings.py loaded")

import logging
from typing import Annotated, Optional
from fastapi import APIRouter, Request, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import UOWDep
from app.services.credentials import CredentialsService
from app.tasks.registry import TASKS



router = APIRouter(
    prefix="/task",
    tags=["Task"],
)


logging.basicConfig(level=logging.INFO, filename="request/task.log",
                    format="%(asctime)s %(levelname)s %(message)s")



@router.post("/add", summary="Создать задачу")
async def add_taks(
    task_type: str,
    params: dict
):
    return {"OK": True}


@router.post("/status", summary="Получить статус задачи")
async def get_status_taks(
    task_type: str,
    task_id: str
):
    return {"OK": True}


@router.post("/remove", summary="Удалить задачу")
async def remove_taks(
    task_type: str,
    task_id: str
):
    
    return {"OK": True}


# from fastapi import APIRouter, HTTPException
# from api.tasks.scheduler import add_task, remove_task, scheduler, task_wrapper
# from api.tasks.example_tasks import sample_task

# sudo systemctl daemon-reload
# sudo systemctl start uvicorn_monitoractivity
# sudo systemctl status uvicorn_monitoractivity
# sudo systemctl enable uvicorn_monitoractivity

# router = APIRouter()

# @router.post("/tasks/add", summary="Добавить задачу")
# async def add_task_endpoint(
#     task_type: str,  # Тип задачи
#     period: int,     # Период выполнения
#     params: dict     # Параметры для задачи
# ):
#     if task_type not in SUPPORTED_TASKS:
#         return {"error": f"Unknown task type: {task_type}"}
    
#     task_id = task_type  # Уникальный task_id для типа задачи

#     # Проверяем, не запущена ли уже задача с этим `task_id`
#     if scheduler.get_job(task_id):
#         return {"error": f"Task '{task_id}' is already running."}

#     # Добавляем задачу
#     task_func = SUPPORTED_TASKS[task_type]["func"]
#     scheduler.add_job(
#         id=task_id,
#         func=task_func,
#         trigger="interval",
#         seconds=period,
#         args=(params,),
#         replace_existing=True  # Перезаписываем, если задача была
#     )
#     return {"message": f"Task '{task_id}' has been added successfully."}


# @router.post("/tasks/add", summary="Добавить задачу")
# async def add_task_endpoint(period: int, param1: int, param2: str):
#     task_id = f"task_{param1}_{param2}"  # task_10_example
#     response = add_task(
#         task_id=task_id,
#         task_func=lambda: task_wrapper(task_id, sample_task, param1, param2),
#         trigger="interval",
#         seconds=period
#     )
#     return {"task_id": task_id, **response}

# @router.post("/tasks/add", summary="Добавить задачу")
# async def add_task_endpoint(task_id: str, period: int, param1: int, param2: str):
#     """
#     Добавить задачу с указанным периодом (в секундах).
#     """
#     if scheduler.get_job(task_id):
#         raise HTTPException(status_code=400, detail="Task already exists.")
#     response = add_task(
#         task_id=task_id,
#         task_func=lambda: task_wrapper(task_id, sample_task, param1, param2),
#         trigger="interval",
#         seconds=period
#     )
#     return response

# @router.delete("/tasks/remove", summary="Удалить задачу")
# async def remove_task_endpoint(task_id: str):
#     """
#     Удалить задачу по идентификатору.
#     """
#     response = remove_task(task_id)
#     return response

# @router.post("/tasks/run", summary="Запустить задачу вручную")
# async def run_task_endpoint(task_id: str, param1: int, param2: str):
#     """
#     Запустить задачу вручную.
#     """
#     if scheduler.get_job(task_id):
#         raise HTTPException(status_code=400, detail="Task is already running.")
#     # Запускаем задачу вручную
#     task_wrapper(task_id, sample_task, param1, param2)
#     return {"status": "success", "message": f"Task {task_id} started manually."}
