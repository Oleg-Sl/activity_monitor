print("app.py loaded")

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.api.routers.routers import all_routers
from app.tasks.scheduler import scheduler, start_scheduler, stop_scheduler, schedule_all_tasks
# from app.tasks.registry import start_scheduler, register_tasks
from app.tasks.sync_entities import sync_entities_task

# from apscheduler.triggers.interval import IntervalTrigger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start_scheduler()
    scheduler.start()
    await schedule_all_tasks()
    # scheduler.add_job()
    # scheduler.add_job(
    #     lambda: print('JOB!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11'),
    #     trigger=IntervalTrigger(minutes=10),
    #     id='currency_update_job',
    #     replace_existing=True
    # )
    yield
    stop_scheduler()


def get_application() -> FastAPI:
    application = FastAPI(
        title="PROJECT_NAME",
        debug=True,
        version="1.0.0",
        root_path="/monitoractivity",
        lifespan=lifespan
    )
    # application.include_router(get_apps_router())

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()

for router in all_routers:
    app.include_router(router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")




@app.get("/")
async def test():
    return {"test": 111}












# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
#     # uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
# if __name__ == "__main__":
#     import os
#     if os.getenv("RUN_MAIN") != "true":
#         uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")



# python app.py
# backend\venv\Scripts\activate.bat
# uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload --log-level debug

# alembic init migrations
# alembic revision --message="Initial" --autogenerate
# alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head

# from app.models.stages import Stages
# from app.models.work_calendar import WorkCalendar
# from app.models.credentials import Credentials
# from app.db.db import Base
