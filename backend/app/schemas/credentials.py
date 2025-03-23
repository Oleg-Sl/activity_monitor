from pydantic import BaseModel, ConfigDict, Field


class CredentialsFormSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    auth_token: str = Field(..., validation_alias='AUTH_ID')
    refresh_token: str = Field(..., validation_alias='REFRESH_ID')


class BitrixClientSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    client_id: str = Field(...)
    client_secret: str = Field(...)


class CredentialSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    domain: str = Field(...)
    auth_token: str = Field(...)
    refresh_token: str = Field(...)

