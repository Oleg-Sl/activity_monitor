from pydantic import BaseModel, ConfigDict, Field


class BitrixSettingsFormSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    auth_token: str = Field(..., validation_alias='ENTITY_ID')
    refresh_token: int | None = Field(..., validation_alias='CATEGORY_ID')



    # id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # domain: Mapped[str] = mapped_column(String(100))
    # auth_token: Mapped[str] = mapped_column(String(100))
    # refresh_token: Mapped[str] = mapped_column(String(100))
    # client_id: Mapped[str] = mapped_column(String(100))
    # client_secret: Mapped[str] = mapped_column(String(100))