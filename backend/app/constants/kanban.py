from .product_schedule import PRODUCTION_SCHEDULE_TYPE_ID
from .production_order import PRODUCTION_ORDER_TYPE_ID


SAWING_AND_ASSEMBLY_KANBAN = [
    {
        'stage': 'plan',
        'title': 'План',
        'code': 'development',
        'entity_type_id': PRODUCTION_SCHEDULE_TYPE_ID,
        'status_id': [
            'DT179_15:UC_D7DURR',
            # 'DT179_15:UC_HXKO7S'
        ]
    },
    {
        'stage': 'expecting',
        'title': 'Ожидание',
        'code': 'development',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_31:UC_HNUB5Y',
            'DT166_31:CLIENT',
            'DT166_29:NEW',
            'DT166_29:3',
            'DT166_29:16'
        ]
    },
    {
        'stage': 'readysawing',
        'title': 'Готов к распилу',
        'code': 'development',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:NEW'
        ]
    },
    {
        'stage': 'sawed',
        'title': 'Пилится',
        'code': 'sawing',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:PREPARATION'
        ]
    },
    {
        'stage': 'awaitingassembly',
        'title': 'Ожидает сборку',
        'code': 'carpentry',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:UC_HV90U6'
        ]
    },
    {
        'stage': 'karskasisgoing',
        'title': 'Карскас собирается',
        'code': 'carpentry_assembly',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:CLIENT'
        ]
    }
]


SAWING_AND_ASSEMBLY_ITEMS = {
    'plan': {
        'title': 'План',
        'code': 'development',
        'entity_type_id': PRODUCTION_SCHEDULE_TYPE_ID,
        'status_id': [
            'DT179_15:UC_D7DURR',
            'DT179_15:UC_HXKO7S'
        ]
    },
    'expecting': {
        'title': 'Ожидание',
        'code': 'development',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_31:UC_HNUB5Y',
            'DT166_31:CLIENT',
            'DT166_29:NEW',
            'DT166_29:3',
            'DT166_29:16'
        ]
    },
    'readysawing': {
        'title': 'Готов к распилу',
        'code': 'development',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:NEW'
        ]
    },
    'sawed': {
        'title': 'Пилится',
        'code': 'sawing',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:PREPARATION'
        ]
    },
    'awaitingassembly': {
        'title': 'Ожидает сборку',
        'code': 'carpentry',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:UC_HV90U6'
        ]
    },
    'karskasisgoing': {
        'title': 'Карскас собирается',
        'code': 'carpentry_assembly',
        'entity_type_id': PRODUCTION_ORDER_TYPE_ID,
        'status_id': [
            'DT166_119:CLIENT'
        ]
    }
}
