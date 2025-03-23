import asyncio
import datetime
# import psycopg2

from app.db.db import async_session_maker
from app.bitrix24.clients.bitrix_client import get_bitrix_client


async def fill_work_calendar(year):
    async with async_session_maker() as db_session:
        bitrix_client = await get_bitrix_client()
        sync_service = SyncService(db_session, bitrix_client)
        await sync_service.sync_all_data()

    # Подключение к БД
    conn = psycopg2.connect(
        dbname="your_db_name",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    WORK_START = datetime.time(9, 0)
    WORK_END = datetime.time(18, 0)
    HOLIDAYS = [datetime.date(2025, 1, 1), datetime.date(2025, 1, 7)]
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)

    current_date = start_date
    while current_date <= end_date:
        is_working_day = current_date.weekday() < 5 and current_date not in HOLIDAYS
        work_start = WORK_START if is_working_day else None
        work_end = WORK_END if is_working_day else None
        description = "Рабочий день" if is_working_day else "Праздник"

        cursor.execute("""
            INSERT INTO work_calendar (date, is_working_day, work_start, work_end, description)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (date) DO NOTHING;
        """, (current_date, is_working_day, work_start, work_end, description))
        current_date += datetime.timedelta(days=1)

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    asyncio.run(fill_work_calendar(datetime.datetime.now().year))
