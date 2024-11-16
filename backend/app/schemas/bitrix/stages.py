from pydantic import BaseModel, ConfigDict, Field



class BitrixStageSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., validation_alias='ID')
    entity_id: str = Field(..., validation_alias='ENTITY_ID')
    category_id: int | None = Field(..., validation_alias='CATEGORY_ID')
    status_id: str = Field(..., validation_alias='STATUS_ID')
    name: str = Field(..., validation_alias='NAME')
    semantic: str | None = Field(..., validation_alias='SEMANTICS')
