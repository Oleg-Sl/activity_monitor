from .bitrix_webhook import BitrixWebhook


async def get_bitrix_client():
    return BitrixWebhook()
