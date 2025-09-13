from app.constants.product_schedule import PRODUCTION_SCHEDULE_TYPE_ID
from app.constants.production_order import PRODUCTION_ORDER_TYPE_ID


# Пилка (Там стадии План, Ожидание, Готов к распилу, Пилеться)
SAWING_KANBAN_SCHEMA = [
    {
        'stage': 'plan',
        'title': 'План',
        'code': 'development',
        'entity_type_id': PRODUCTION_SCHEDULE_TYPE_ID,
        'status_id': [
            'DT179_15:UC_D7DURR',
        ]
    },
    {
        'stage': 'expecting',
        'title': 'Ожидание',
        'code': 'development',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_31:UC_HNUB5Y',   # Технолог (№2 - Александр)
            'DT166_31:CLIENT',      # Технолог (№1 - Валерия)
        ]
    },
    {
        'stage': 'readysawing',
        'title': 'Готов к распилу',
        'code': 'development',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:NEW'     # Ждет запуска
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
]
