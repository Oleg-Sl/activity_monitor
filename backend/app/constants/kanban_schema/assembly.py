from app.constants.product_schedule import PRODUCTION_SCHEDULE_TYPE_ID
from app.constants.production_order import PRODUCTION_ORDER_TYPE_ID


# - Сборка ( План, Пилеться, Ожидает сборка, Сборка каркаса)
ASSEMBLY_KANBAN_SCHEMA = [
    {
        'stage': 'plan',
        'title': 'План',
        'code': 'development',
        'entity_type_id': PRODUCTION_SCHEDULE_TYPE_ID,
        'status_id': [
            'DT179_15:UC_NQTWXF',   # План для сборки
        ]
    },
    {
        'stage': 'sawed',
        'title': 'Пилится',
        'code': 'sawing',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:PREPARATION'     # Распиловка
        ]
    },
    {
        'stage': 'awaitingassembly',
        'title': 'Ожидает сборку',
        'code': 'carpentry',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:UC_HV90U6'   # Ждет Сборки
        ]
    },
    {
        'stage': 'karskasisgoing',
        'title': 'Карскас собирается',
        'code': 'carpentry_assembly',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:CLIENT'  # Сборка каркасов
        ]
    }
]
