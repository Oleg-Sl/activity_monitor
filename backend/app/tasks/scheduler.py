from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError
from apscheduler.triggers.cron import CronTrigger
from pytz import utc
from typing import Callable, Any
import logging

from .update_calendar import update_calendar_task
from .sync_stages import sync_stages_task
from .production_order_events import sync_production_events_task
from .production_schedule_events import sync_production_schedule_events_task

logger = logging.getLogger(__name__)


scheduler = AsyncIOScheduler(timezone=utc)
running_tasks = {}


TASKS = {
    "update_calendar": {
        "func": update_calendar_task,
        "description": "Update status of days",
        "trigger": CronTrigger(month=1, day=1, hour=1, minute=7),
        "params": {
            # "months": 1
        }
    },
    "sync_stages": {
        "func": sync_stages_task,
        "description": "Sync the stages of the database with bitrix24.",
        "trigger": "interval",
        "params": {
            "weeks": 1
        }
    },
    "event_production_orders": {
        "func": sync_production_events_task,
        "description": "Get event of entities and save it to the database with bitrix24.",
        "trigger": "interval",
        "params": {
            "minutes": 2
        }
    },
    "event_production_schedules": {
        "func": sync_production_schedule_events_task,
        "description": "Get event of entities and save it to the database with bitrix24.",
        "trigger": "interval",
        "params": {
            "minutes": 2
        }
    },
}


async def schedule_all_tasks():
    """Запускает все регулярные задачи из TASKS."""
    for task_id, task_data in TASKS.items():
        await add_task(task_id, task_data["func"], task_data["trigger"], **task_data["params"])
    logger.info(f"Все задачи успешно запланированы.")

    print("Все задачи успешно запланированы.")


def start_scheduler():
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()


async def task_wrapper(task_id: str, task_func: Callable, *args, **kwargs):
    """Обертка для предотвращения повторного запуска задачи с тем же идентификатором."""
    print(f"Старт задачи {task_id}")
    logger.info(f"Запуск задачи {task_id}...")

    if running_tasks.get(task_id):
        print(f"Задача {task_id} уже выполняется. Запуск отменен.")
        return
    
    running_tasks[task_id] = True
    try:
        await task_func(*args, **kwargs)
    except Exception as e:
        print(f"Ошибка в задаче {task_id}: {e}")
    finally:
        running_tasks.pop(task_id, None)


async def add_task(
    task_id: str, 
    task_func: Callable, 
    trigger: str = "interval", 
    **trigger_args
):
    """
    Добавить задачу в планировщик.
    - `task_id`: уникальный идентификатор задачи.
    - `task_func`: асинхронная функция задачи.
    - `trigger`: тип триггера (например, 'interval' или 'cron').
    - `trigger_args`: параметры триггера.
    """
    print(f"Добавляем задачу {task_id} с триггером {trigger} и параметрами {trigger_args}")

    try:
        scheduler.add_job(
            task_wrapper,
            id=task_id,
            # func=task_wrapper,
            args=[task_id, task_func],
            trigger=trigger,
            replace_existing=True,
            **trigger_args
        )
        return {"status": "success", "message": f"Task {task_id} added."}
    except Exception as e:
        print(e)
        return {"status": "error", "message": str(e)}


def remove_task(task_id: str):
    """Удалить задачу из планировщика."""
    try:
        scheduler.remove_job(task_id)
        running_tasks.pop(task_id, None)
        return {"status": "success", "message": f"Task {task_id} removed."}
    except JobLookupError:
        return {"status": "error", "message": f"Task {task_id} not found."}
