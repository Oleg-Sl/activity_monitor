# from schemas.tasks import TaskHistorySchemaAdd, TaskSchemaAdd, TaskSchemaEdit
# from utils.repository import AbstractRepository
from app.utils.unitofwork import IUnitOfWork
from app.schemas.credentials import CredentialsFormSchema, BitrixClientSchema
from app.repositories.credentials import BitrixCredentialsRepository


# class ClientsService:
#     async def add_client(self, uow: IUnitOfWork, client_data: BitrixClientSchema):
#         client_dict = client_data.model_dump()
#         async with uow:
#             client_id


class CredentialsService:
    async def add_credential(self, uow: IUnitOfWork, credential: CredentialsFormSchema):
        credential_dict = credential.model_dump()
        async with uow:
            credential_id = await uow.credentials.add_one(credential_dict)
            await uow.commit()
            return credential_id

    async def get_credentials(self, uow: IUnitOfWork):
        async with uow:
            credentials = await uow.credentials.find_all()
            return credentials

    async def edit_credential(self, uow: IUnitOfWork, credential_id: int, credential: BitrixClientSchema):
        credential_dict = credential.model_dump()
        async with uow:
            curr_credential = await uow.credentials.edit_one(credential_id, credential_dict)
            await uow.commit()

    # async def get_task_history(self, uow: IUnitOfWork):
    #     async with uow:
    #         history = await uow.task_history.find_all()
    #         return history
