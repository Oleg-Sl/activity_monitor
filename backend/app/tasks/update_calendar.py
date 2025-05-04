import asyncio
import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_maker
from backend.app.repositories.work_calendar_repository import WorkCalendarRepository


async def update_calendar_task(session: AsyncSession, year: int = None):
    if year is None:
        year = datetime.now().year + 1

    try:
        WORK_START = datetime.time(8, 0)
        WORK_END = datetime.time(17, 0)
        HOLIDAYS = [
            datetime.date(year, 1, 1),
            datetime.date(year, 1, 2),
            datetime.date(year, 1, 3),
            datetime.date(year, 1, 4),
            datetime.date(year, 1, 5),
            datetime.date(year, 1, 6),
            datetime.date(year, 1, 7),
        ]
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)

        calendar_repository = WorkCalendarRepository(session)

        current_date = start_date
        while current_date <= end_date:
            is_working_day = current_date.weekday() < 5 and current_date not in HOLIDAYS
            work_start = WORK_START if is_working_day else None
            work_end = WORK_END if is_working_day else None
            description = "Рабочий день" if is_working_day else "Праздник"

            result_id = await calendar_repository.create_if_not_exist({
                    "date": current_date,
                    "is_working_day": is_working_day,
                    "work_start": work_start,
                    "work_end": work_end,
                    "description": description
                })

            current_date += datetime.timedelta(days=1)

        await session.commit()
        print(f"Календарь успешно обновлён для {year} года.")
    except Exception as e:
        print(f"Ошибка при обновлении календаря: {e}")


async def main():
    async with async_session_maker() as session:
        await update_calendar_task(session, 2025)


if __name__ == "__main__":
    asyncio.run(main())

# python -m app.tasks.update_calendar
