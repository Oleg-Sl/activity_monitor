from sqlalchemy.ext.asyncio import AsyncSession

from .bitrix_client_token import BitrixClient as TokenBitrixClient
# from .bitrix_client_webhook import BitrixClient as WebhookBitrixClient
from .bitrix_client import InterfaceBitrixClient
from app.repositories.credentials import CredentialRepository


def get_bitrix_client(session: AsyncSession) -> InterfaceBitrixClient:
    # return WebhookBitrixClient()
    credential_repository = CredentialRepository(session)
    return TokenBitrixClient(credential_repository)

