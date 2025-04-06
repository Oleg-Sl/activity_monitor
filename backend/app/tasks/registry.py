from .update_calendar import update_calendar_task
from .sync_stages import sync_stages_task
from .sync_entities import sync_entities_task
from .event_entities import event_entities_task
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()


TASKS = {
    "update_calendar": {
        "func": update_calendar_task,
        "description": "Update status of days"
    },
    "sync_stages": {
        "func": sync_stages_task,
        "description": "Sync the stages of the database with bitrix24."
    },
    "sync_entities": {
        "func": sync_entities_task,
        "description": "Sync the entities of the database with bitrix24."
    },
    "event_entities": {
        "func": event_entities_task,
        "description": "Get event of entities and save it to the database with bitrix24."
    },
}


def register_tasks(func, minutes, job_id):
    print(f"task {job_id} is registry")
    scheduler.add_job(func, 'interval', minutes=minutes, id=job_id)


def start_scheduler():
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()
