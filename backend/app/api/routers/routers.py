
from .bitrix import router as router_bitrix
from .monitoring import router as router_monitroing
from .tasks import router as router_task

all_routers = [
    router_bitrix,
    router_monitroing,
    router_task,
]
