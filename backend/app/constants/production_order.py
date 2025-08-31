
PRODUCTION_ORDER_TYPE_ID = 166    # ID смартпроцесса производство

PRODUCTION_ORDER_EVENT_NAMES = [
    'ONCRMDYNAMICITEMADD_166',
    'ONCRMDYNAMICITEMUPDATE_166',
]

PRODUCTION_ORDER_DATA = {
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


# Идентификаторы значений списка поля "Тип изделия"
PRODUCTION_ORDER_TYPE_OF_PRODUCT = {
    5359: PRODUCTION_ORDER_DATA['sofa'],
    5361: PRODUCTION_ORDER_DATA['bed'],
    5363: PRODUCTION_ORDER_DATA['armchair'],
    5365: PRODUCTION_ORDER_DATA['pouf'],
    5367: PRODUCTION_ORDER_DATA['msp'],
    5369: PRODUCTION_ORDER_DATA['nightstand'],
    5371: PRODUCTION_ORDER_DATA['table'],
    5373: PRODUCTION_ORDER_DATA['chair'],
    5375: PRODUCTION_ORDER_DATA['melochevka'],

    5543: PRODUCTION_ORDER_DATA['exhibition'],
    5923: PRODUCTION_ORDER_DATA['workshop']
}
