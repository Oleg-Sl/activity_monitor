from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.constants.production_order import PRODUCTION_ORDER_TYPE_OF_PRODUCT


class ProductOrderInSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: int = Field(..., validation_alias='id')
    title: str = Field(..., validation_alias='title')
    entity_type_id: int = Field(..., validation_alias='entityTypeId')

    created_time: Optional[datetime] = Field(..., validation_alias='createdTime')
    updated_time: datetime = Field(..., validation_alias='updatedTime')

    created_by: int = Field(..., validation_alias='createdBy')
    assigned_by_id: Optional[int] = Field(..., validation_alias='assignedById')
    company_id: Optional[int] = Field(..., validation_alias='companyId')
    category_id: Optional[int] = Field(..., validation_alias='categoryId')

    moved_time: Optional[datetime] = Field(..., validation_alias='movedTime')
    moved_by: Optional[int] = Field(..., validation_alias='movedBy')
    stage_id: Optional[int] = Field(None)
    stage_id_str: Optional[str] = Field(..., validation_alias='stageId')
    previous_stage_id: Optional[str] = Field(..., validation_alias='previousStageId')

    opportunity: Optional[float] = Field(..., validation_alias='opportunity')
    product_id: Optional[int] = Field(..., validation_alias='ufCrm21_1726480119')
    product_type: Optional[int] = Field(..., validation_alias='ufCrm21_1726637267')

    fabric_arrival_date: Optional[str] = None

    name: Optional[str] = None
    product_type_str: Optional[str] = None

    image_url: Optional[str] = None
    image_token: Optional[str] = None
    image_local_path: Optional[str] = None

    allocated_hours: Optional[float] = Field(..., validation_alias='ufCrm21_1745248795')
    priority: Optional[float] = None
    production_date: Optional[datetime] = None

    @model_validator(mode="before")
    def extract_image_url(cls, data):
        if "ufCrm21_1745248739" in data and isinstance(data["ufCrm21_1745248739"], dict):
            data["image_url"] = data["ufCrm21_1745248739"].get("urlMachine")

        return data
    
    @model_validator(mode="before")
    def extract_product_name(cls, data):
        if 'ufCrm21_1726637267' in data:
            product_type_id = data['ufCrm21_1726637267']
            meta_data = PRODUCTION_ORDER_TYPE_OF_PRODUCT.get(product_type_id, {})
            data['name'] = meta_data.get('name')
            data['product_type_str'] = meta_data.get('product_type')

        return data
