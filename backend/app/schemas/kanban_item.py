from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# from app.schemas.product_order_schema import ProductOrderInSchema


class KanbanItemSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    stage: str
    title: str
    code: str
    entity_type_id: int
    status_id: List[str]
    productions: Optional[List] = []
