import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# # from app.tasks import update_work_calendar
# # from app.database import async_session
# from app.db.db import async_session_maker


# scheduler = AsyncIOScheduler()


# def configure_scheduler():
#     async def scheduled_update_calendar():
#         async with async_session_maker() as session:
#             current_year = datetime.datetime.now().year
#             await update_work_calendar(session, current_year)

#     # Добавление задачи по расписанию
#     scheduler.add_job(
#         scheduled_update_calendar,
#         CronTrigger(year="*", month="1", day="1", hour="2", minute="0"),
#         id="update_calendar",
#         replace_existing=True
#     )

#     scheduler.start()

