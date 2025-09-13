from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer, String, Float, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime

from app.db.session import Base


# Смарт процесс в "производство - цех"


class ProductionOrder(Base):
    __tablename__ = 'production_order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Идентификатор", autoincrement=True)
    entity_id: Mapped[int] = mapped_column(Integer, comment="Идентификатор из битрикс")
    title: Mapped[Optional[str]] = mapped_column(String(255), comment="Название смарт-процесса в битрикс")
    entity_type_id: Mapped[Optional[int]] = mapped_column(Integer, comment="Идентификатор типа смарт процесса")

    deal_id: Mapped[Optional[int]] = mapped_column(Integer, comment="ID_сделки (для монитора)")

    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Когда создан")
    updated_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Когда обновлён")

    created_by: Mapped[int] = mapped_column(Integer, comment="Кем создан - числовой идентификатор")
    assigned_by_id: Mapped[int] = mapped_column(Integer, comment="Ответственный -  числовой идентификатор")
    company_id: Mapped[Optional[int]] = mapped_column(Integer, comment="Компания -  числовой идентификатор")
    category_id: Mapped[Optional[int]] = mapped_column(Integer, comment="Воронка - числовой идентификатор")

    moved_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Когда передвинут - числовой идентификатор")
    moved_by: Mapped[int] = mapped_column(Integer, comment="Кем передвинут - числовой идентификатор")
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey('stages.id'), comment="Стадия - числовой идентификатор")
    stage_id_str: Mapped[str] = mapped_column(String(255), comment="Стадия - абревиатура")
    previous_stage_id: Mapped[str] = mapped_column(String(255), comment="Предыдущая стадия - абревиатура")

    opportunity: Mapped[Optional[float]] = mapped_column(Float, comment="Сумма")
    product_id: Mapped[Optional[int]] = mapped_column(Integer, comment="ID смарта изделия")
    product_type: Mapped[Optional[int]] = mapped_column(Integer, comment="Тип изделия - числовой код")

    fabric_arrival_date: Mapped[Optional[str]] = mapped_column(String(255), comment="Дата прихода ткани")

    name: Mapped[Optional[str]] = mapped_column(String(255), comment="Имя изделия")
    product_type_str: Mapped[Optional[str]] = mapped_column(String(255), comment="Аббревиатура типа изделия")
    
    image_url: Mapped[Optional[str]] = mapped_column(String(2048), comment="url фотографии")
    image_token: Mapped[Optional[str]] = mapped_column(String(2048), comment="Уникальный токен фотографии изделия (из url)")
    image_local_path: Mapped[Optional[str]] = mapped_column(String(255), comment="Путь к фотографии на сервере")

    priority: Mapped[Optional[str]] = mapped_column(String(16), comment="Приоритет")
    production_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), comment="Дата производства")

    allocated_hours: Mapped[Optional[float]] = mapped_column(Float, comment="Выделено часов на стадии")

    # stage_histories = relationship("StageHistory", back_populates="production_order")

    # production_stage_history = relationship("ProductionStageHistory", backref="production_order")
    production_stage_histories = relationship("ProductionStageHistory", back_populates="production_order")

    def __repr__(self):
        return (
            f"<ProductionOrder(id={self.id}, "
            f"title='{self.title}', "
            f"stage_id_str='{self.stage_id_str}', "
            f"name='{self.name}')>"
        )

# python -m alembic revision --autogenerate -m "initial"
# python -m alembic revision --autogenerate -m "Add fields to entity model"
# python -m alembic upgrade head
