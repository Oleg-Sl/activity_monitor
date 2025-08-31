from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime, time, timedelta


class BitrixEntitiesSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # history_id SERIAL PRIMARY KEY,
    # product_id INT REFERENCES products(product_id),
    # stage_id INT REFERENCES stages(stage_id),
    # start_time TIMESTAMP,
    # end_time TIMESTAMP,
    # -- Дополнительные поля для учёта рабочего/не рабочего времени
    # work_time INTERVAL,  -- Время, которое изделие провело на стадии, с учётом рабочего времени
    # non_work_time INTERVAL 

    # id : str = Field(..., validation_alias='id')
    # created_time: datetime  = Field(..., validation_alias='createdTime')
    # updated_time: datetime  = Field(..., validation_alias='updatedTime')
    # created_by: int = Field(..., validation_alias='createdBy')
    # assigned_by_id: int = Field(..., validation_alias='assignedById')
    # company_id: int = Field(..., validation_alias='companyId')
    # category_id: int = Field(..., validation_alias='categoryId')                    # Воронка
    # moved_time: datetime  = Field(..., validation_alias='movedTime')                # Когда передвинут
    # moved_by: int = Field(..., validation_alias='movedBy')                          # Кем передвинут
    # stage_id: int = Field(..., validation_alias='stageId')                          # Стадия
    # previous_stage_id: int = Field(..., validation_alias='previousStageId')         # Предыдущая стадия
    # opportunity: float = Field(..., validation_alias='opportunity')                 # Сумма
    # parent_deal: float = Field(..., validation_alias='parentId2')                   # Сделка
    # item_ready_date: date = Field(..., validation_alias='ufCrm21_1708176725')       # Дата приема готовности изделия
    # pack_date: date = Field(..., validation_alias='ufCrm21_1708176767')             # Дата упаковки
    # item_id: int = Field(..., validation_alias='ufCrm21_1705725754')                # ID_товарной позиции
    # cost_price: float = Field(..., validation_alias='ufCrm21_1705725831')           # Себестоимость изделия
    # shop_entry_date: date = Field(..., validation_alias='ufCrm21_1705725937')       # Дата поступления в цех
    # design_end_date: date = Field(..., validation_alias='ufCrm21_1705725978')       # Дата завершения проектирования
    # contract_due_date: date = Field(..., validation_alias='ufCrm21_1707632545')     # Дата сдачи по договору
    # agreed_log_date: datetime  = Field(..., validation_alias='ufCrm21_1709468710')  # Дата логистика (согласованная)
    # actual_ship_date: date = Field(..., validation_alias='ufCrm21_1711276851')      # Дата фактической отгрузки
    # product_type: int = Field(..., validation_alias='ufCrm21_1726637267')           # Тип изделия
    # forecast_ready_date: date = Field(..., validation_alias='ufCrm21_1734528164')   # Дата ПРОГНОЗ готовности
    # work_start_date: datetime  = Field(..., validation_alias='ufCrm21_1730035261')  # Дата старта (принят в работу)




