from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date


class BitrixEntitiesSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., validation_alias='id')
    title: str = Field(..., validation_alias='title')
    created_time: datetime | None = Field(..., validation_alias='createdTime')
    updated_time: datetime = Field(..., validation_alias='updatedTime')
    created_by: int = Field(..., validation_alias='createdBy')
    assigned_by_id: int | None = Field(..., validation_alias='assignedById')
    company_id: int | None = Field(..., validation_alias='companyId')
    category_id: int | None = Field(..., validation_alias='categoryId')

    moved_time: datetime | None = Field(..., validation_alias='movedTime')
    moved_by: int | None = Field(..., validation_alias='movedBy')
    stage_id: str | None = Field(..., validation_alias='stageId')
    previous_stage_id: str | None = Field(..., validation_alias='previousStageId')
    opportunity: float | None = Field(..., validation_alias='opportunity')
    product_id: int | None = Field(..., validation_alias='ufCrm21_1726480119')
    product_id: int | None = Field(..., validation_alias='ufCrm21_1726637267')
