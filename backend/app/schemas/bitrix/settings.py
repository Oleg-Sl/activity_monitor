from pydantic import BaseModel, ConfigDict, Field


class BitrixSettingsFormSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    auth_token: str = Field(..., validation_alias='AUTH_ID')
    refresh_token: str = Field(..., validation_alias='REFRESH_ID')

    # id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # domain: Mapped[str] = mapped_column(String(100))
    # auth_token: Mapped[str] = mapped_column(String(100))
    # refresh_token: Mapped[str] = mapped_column(String(100))
    # client_id: Mapped[str] = mapped_column(String(100))
    # client_secret: Mapped[str] = mapped_column(String(100))
