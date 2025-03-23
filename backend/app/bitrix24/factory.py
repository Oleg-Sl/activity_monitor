from .bitrix_client_token import BitrixClient as TokenBitrixClient
from .bitrix_client_webhook import BitrixClient as WebhookBitrixClient
from .bitrix_client import InterfaceBitrixClient


def get_bitrix_client() -> InterfaceBitrixClient:
    return WebhookBitrixClient()
    # return TokenBitrixClient()

