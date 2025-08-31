BASE_URL = 'http://127.0.0.1:8888'

BASE_DIR = r'C:\projects\activity_monitor\backend'
PATCH_TO_UPLOADS = r'static\uploads'

KANBAN_ITEMS = {
    'expecting': {
        'title': 'Ожидание',
        'code': 'development',
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
        'status_id': [
            'DT166_119:NEW'
        ]
    },
    'sawed': {
        'title': 'Пилится',
        'code': 'sawing',
        'status_id': [
            'DT166_119:PREPARATION'
        ]
    },
    'awaitingassembly': {
        'title': 'Ожидает сборку',
        'code': 'carpentry',
        'status_id': [
            'DT166_119:UC_HV90U6'
        ]
    },
    'karskasisgoing': {
        'title': 'Карскас собирается',
        'code': 'carpentry_assembly',
        'status_id': [
            'DT166_119:CLIENT'
        ]
    }
}

PRODUCT_TYPE_DATA = {
    'sofa': {
        'product_type': 'sofa',
        'name': 'Диван',
        'is_product': True,
        'entity_type_id': '158',
        'fields': {
            'image': "ufCrm53_1713496168",
            'fot_id': 'parentId1048'
        }
    },
    'bed': {
        'product_type': 'bed',
        'name': 'Кровать',
        'is_product': True,
        'entity_type_id': '189',
        'fields': {
            'image': "ufCrm61_1713510411",
            'fot_id': 'parentId1048'
        }
    },
    'armchair': {
        'product_type': 'armchair',
        'name': 'Кресло',
        'is_product': True,
        'entity_type_id': '165',
        'fields': {
            'image': "ufCrm57_1713503043",
            'fot_id': 'parentId1048'
        }
    },
    'pouf': {
        'keproduct_typey': 'pouf',
        'name': 'Пуф',
        'is_product': True,
        'entity_type_id': '167',
        'fields': {
            'image': "ufCrm67_1713518917",
            'fot_id': 'parentId1048'
        }
    },
    'msp': {
        'product_type': 'msp',
        'name': 'МСП',
        'is_product': True,
        'entity_type_id': '172',
        'fields': {
            'image': "ufCrm23_1706606863",
            'fot_id': 'parentId1048'
        }
    },
    'nightstand': {
        'product_type': 'nightstand',
        'name': 'Тумба',
        'is_product': True,
        'entity_type_id': '188',
        'fields': {
            'image': "ufCrm73_1714011366",
            'fot_id': 'parentId1048'
        }
    },
    'table': {
        'product_type': 'table',
        'name': 'Стол',
        'is_product': True,
        'entity_type_id': '186',
        'fields': {
            'image': "ufCrm75_1714013720",
            'fot_id': 'parentId1048'
        }
    },
    'chair': {
        'product_type': 'chair',
        'name': 'Стул',
        'is_product': True,
        'entity_type_id': '150',
        'fields': {
            'image': "ufCrm77_1714055062",
            'fot_id': 'parentId1048'
        }
    },
    'melochevka': {
        'product_type': 'melochevka',
        'name': 'Мелочевка',
        'is_product': True,
        'entity_type_id': '162',
        'fields': {
            'image': "ufCrm63_1713514588",
            'fot_id': 'parentId1048'
        }
    },
    'exhibition': {
        'product_type': 'exhibition',
        'name': 'С выставки (шоу рум)',
        'is_product': False
    },
    'workshop': {
        'product_type': 'workshop',
        'name': 'Работа по цеху',
        'is_product': False
    }
}


WORKSHOP_TYPE_OF_PRODUCT = {
    5359: PRODUCT_TYPE_DATA['sofa'],
    5361: PRODUCT_TYPE_DATA['bed'],
    5363: PRODUCT_TYPE_DATA['armchair'],
    5365: PRODUCT_TYPE_DATA['pouf'],
    5367: PRODUCT_TYPE_DATA['msp'],
    5369: PRODUCT_TYPE_DATA['nightstand'],
    5371: PRODUCT_TYPE_DATA['table'],
    5373: PRODUCT_TYPE_DATA['chair'],
    5375: PRODUCT_TYPE_DATA['melochevka'],

    5543: PRODUCT_TYPE_DATA['exhibition'],
    5923: PRODUCT_TYPE_DATA['workshop']
}


ALLOCATED_HOURS  = {
    'development': 'ufCrm93_1726817717',              # Разработка
    'sawing': 'ufCrm93_1726817766',                   # Пилка
    'assembly': 'ufCrm93_1726817832',                 # Сборка
    'ppu': 'ufCrm93_1726817923',                      # ППУ
    'sewing': 'ufCrm93_1726817944',                   # Швейка
    'covering': 'ufCrm93_1726817965',                 # Обтяжка
    'carpentry': 'ufCrm93_1726817986',                # Столярка
    'carpentry_assembly': 'ufCrm93_1726818006',       # Столярка (сборка)
    'painting_preparation': 'ufCrm93_1726818054',     # Покраска (подготовка)
    'painting': 'ufCrm93_1726818030',                 # Покраска
}

ZAKUP_FIELDS = {
    'fabric_arrival_date': 'ufCrm5_1727592610'
}