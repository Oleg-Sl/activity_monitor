import copy
import datetime
from typing import List, Optional
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

# from app.constants.production_order import PRODUCTION_ORDER_TYPE_OF_PRODUCT
# from app.constants.common import PRODUCTION_ORDER_TYPE_ID
from app.core.config import BASE_DIR, BASE_URL
from app.services.bitrix24.bitrix_client import InterfaceBitrixClient
from app.schemas.product_order_schema import ProductOrderInSchema
from app.infrastructure.file_downloader.file_downloader import FileDownloader
from app.services.file_service import FileServiceFactory
from app.repositories.production_order_repository import ProductionOrderRepository
from app.repositories.stage_history_repository import StageHistoryRepository
from app.repositories.work_calendar_repository import WorkCalendarRepository
from app.repositories.stage_repository import StageRepository
from app.models.stage import Stages
from app.models.production_order import ProductionOrder
from app.models.production_schedule import ProductionSchedule
from app.repositories.production_order_repository import ProductionOrderRepository
from app.repositories.production_schedule_repository import ProductionScheduleRepository
from app.services.workcalendar_service import WorkCaldendarService


class ProductionService:
    def __init__(self, production_order_repo: ProductionOrderRepository, calendar_service: WorkCaldendarService):
        self.order_repo = production_order_repo
        self.calendar_service = calendar_service
        # self.production_schedule = production_schedule_repo

    # async def get_production_schedules(self) -> List:
    #     statuses_ids = ['DT179_15:UC_D7DURR', 'DT179_15:UC_HXKO7S',]
    #     productions = await self.production_schedule.filter(ProductionSchedule.stage_id_str.in_(statuses_ids))
    #     result = []
    #     for production in productions:
    #         result.append({
    #             "id": production.id,
    #             "name": production.name,
    #             "allocated_hours": None,
    #             "stage_id": production.stage_id,
    #             "stage_str": production.stage_id_str,
    #             "stage_duration_seconds": None,
    #             "stage_duration_hours": None,
    #             "hours_left": None,
    #             "fabric_arrival_date": None,
    #             "image": None,
    #             "production_date": production.production_date,
    #             "priority": production.priority,
    #         })

    #     ind = 0
    #     for production in result:
    #         if production['priority']:
    #             if production['priority'] == '01':
    #                 production["color"] = "#FF0000"
    #             elif production['priority'] == 1:
    #                 production["color"] = "#FFA500"
    #             elif production['priority'] == 2:
    #                 production["color"] = "#FFFF00"
    #         else:
    #             if ind == 0:
    #                 production["color"] = "#FF0000"
    #             elif ind == 1:
    #                 production["color"] = "#FFA500"
    #             elif ind == 2:
    #                 production["color"] = "#FFFF00"
    #             ind += 1

    #     return result

    async def get_kanban_data(self, kanban_config: List) -> List:
        result = [{**stage, 'productions': []} for stage in copy.deepcopy(kanban_config)]
        now = datetime.datetime.now(datetime.timezone.utc)

        all_statuses_ids = sum((v['status_id'] for v in kanban_config), [])
        productions = await self.order_repo.filter(ProductionOrder.stage_id_str.in_(all_statuses_ids))

        for production in productions:
            current_stage_obj = None
            for stage_obj in result:
                if production.stage_id_str in stage_obj['status_id']:
                    current_stage_obj = stage_obj
                    break
            
            if current_stage_obj is None:
                continue

            elapsed_time = await self.calendar_service.calculate_work_time(production.moved_time, now)
            hours_left = (production.allocated_hours - elapsed_time.total_seconds() / 3600) if elapsed_time and production.allocated_hours else '-'
            current_stage_obj['productions'].append({
                "id": production.id,
                "name": production.name,
                "stage_id": production.stage_id,
                "stage_str": production.stage_id_str,
                "allocated_hours": production.allocated_hours,
                "stage_duration_seconds": elapsed_time.total_seconds() if elapsed_time else None,
                "stage_duration_hours": elapsed_time.total_seconds() / 3600 if elapsed_time else None,
                "elapsed_time": (now - production.moved_time)  / 3600,
                "hours_left": hours_left,
                "fabric_arrival_date": production.fabric_arrival_date,
                "image": f'{BASE_URL}/{production.image_local_path}' if production.image_local_path else None,
                "production_date": production.production_date,
                "priority": None,
                "color": None
            })

        for stage_obj in result:
            ind = 0
            for production in stage_obj['productions']:
                if production['priority']:
                    if production['priority'] == '01':
                        production["color"] = "#FF0000"
                    elif production['priority'] == 1:
                        production["color"] = "#FFA500"
                    elif production['priority'] == 2:
                        production["color"] = "#FFFF00"
                else:
                    if ind == 0:
                        production["color"] = "#FF0000"
                    elif ind == 1:
                        production["color"] = "#FFA500"
                    elif ind == 2:
                        production["color"] = "#FFFF00"
                    ind += 1

        for stage_obj in result:
            if stage_obj['stage'] == 'plan':
                productitons = await self.get_plan_stage(stage_obj['status_id'])
                stage_obj['productions'].extend(productitons)

        return result


    async def get_orders_grouped_by_stage(self, kanban_config: dict) -> dict:
        result = {key: [] for key in kanban_config}
        now = datetime.datetime.now(datetime.timezone.utc)

        all_statuses_ids = sum((v['status_id'] for v in kanban_config.values()), [])

        order_entities = await self.order_repo.filter(ProductionOrder.stage_id_str.in_(all_statuses_ids))

        for entity in order_entities:
            current_group = None
            for group_key, group_data in kanban_config.items():
                if entity.stage_id_str in group_data['status_id']:
                    current_group = group_key
                    break

            if current_group is None:
                continue

            # stmt = select(StageHistory).where(
            #     StageHistory.work_order_id == entity.id,
            #     StageHistory.end_time.is_(None)
            # )
            # stage_result = await self.session.execute(stmt)
            # print(stage_result)
            # current_stage = stage_result.scalars().first()
            # print('current_stage = ', current_stage)
            # total_time = None
            # if current_stage:
            #     total_time = now - current_stage.start_time

            # total_time = now - entity.moved_time
            elapsed_time = await self.calendar_service.calculate_work_time(entity.moved_time, now)

            hours_left = (entity.allocated_hours - elapsed_time.total_seconds() / 3600) if elapsed_time and entity.allocated_hours else '-'

            self.calendar_service
            result[current_group].append({
                "id": entity.id,
                "name": entity.name,
                "stage_id": entity.stage_id,
                "stage_str": entity.stage_id_str,
                "allocated_hours": entity.allocated_hours,
                "stage_duration_seconds": elapsed_time.total_seconds() if elapsed_time else None,
                "stage_duration_hours": elapsed_time.total_seconds() / 3600 if elapsed_time else None,
                "elapsed_time": (now - entity.moved_time)  / 3600,
                "hours_left": hours_left,
                "fabric_arrival_date": entity.fabric_arrival_date,
                "image": f'{BASE_URL}/{entity.image_local_path}' if entity.image_local_path else None,
                "production_date": entity.production_date,
                "priority": None,
                "color": None
            })

        for group in result:
            ind = 0
            for production in result[group]:
                if production['priority']:
                    if production['priority'] == '01':
                        production["color"] = "#FF0000"
                    elif production['priority'] == 1:
                        production["color"] = "#FFA500"
                    elif production['priority'] == 2:
                        production["color"] = "#FFFF00"
                else:
                    if ind == 0:
                        production["color"] = "#FF0000"
                    elif ind == 1:
                        production["color"] = "#FFA500"
                    elif ind == 2:
                        production["color"] = "#FFFF00"
                    ind += 1

        return result

    
    async def get_plan_stage(self, stages: List[str]):
        week_start, week_end = self.get_week_timeframe()

        completed_production_orders = await self.order_repo.get_completed(stages, week_start, week_end)
        print('completed_production_orders = ', completed_production_orders)
        result = []
        for production in completed_production_orders:
            result.append({
                "id": production.id,
                "name": production.name,
                "stage_id": production.stage_id,
                "stage_str": production.stage_id_str,
                "allocated_hours": production.allocated_hours,
                "stage_duration_seconds": None,
                "stage_duration_hours": None,
                "elapsed_time": None,
                "hours_left": 0,
                "fabric_arrival_date": None,
                "image": f'{BASE_URL}/{production.image_local_path}' if production.image_local_path else None,
                "production_date": production.production_date,
                "priority": None,
                "color": "#00D624"
            })
        
        return result
    
    def get_week_timeframe(self):
        today = datetime.datetime.now()
        start = today - datetime.timedelta(days=today.weekday())
        end = start + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)
        return start, end