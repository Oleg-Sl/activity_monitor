from app.utils.unitofwork import IUnitOfWork
from app.schemas.credentials import CredentialsFormSchema, BitrixClientSchema


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
