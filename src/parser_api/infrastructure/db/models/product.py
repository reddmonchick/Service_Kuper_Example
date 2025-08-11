from __future__ import annotations

from src.parser_api.infrastructure.db.models.base import Base
from src.parser_api.schemas.models import ProductDetailDTO, StoreDTO, CategoryDTO, ProductDTO
from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, BigInteger  

class Product(Base):
    __tablename__ = "Products"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    photos = Column(JSON)
    price_basic = Column(Integer)
    price_with_discount = Column(Integer)
    discount_size = Column(Integer)
    quantity_rate = Column(Integer)
    description = Column(String)
    options = Column(JSON)
    category_name = Column(String)
    category_id = Column(Integer)
    store_name = Column(String)
    store_id = Column(Integer)
    query = Column(String)

    @classmethod
    def from_dto(self, product_detail: ProductDetailDTO):
        BASIC_INFO: ProductDTO = product_detail.basic_info
        CATEGORY_INFO: CategoryDTO = product_detail.category
        STORE_INFO: StoreDTO = product_detail.category.store

        return Product(
            id=BASIC_INFO.id,
            name=BASIC_INFO.name,
            photos=BASIC_INFO.photos,
            price_basic=BASIC_INFO.price_basic,
            price_with_discount=BASIC_INFO.price_with_discount,
            discount_size=BASIC_INFO.discount_size,
            quantity_rate=product_detail.quantity_rate,
            description=product_detail.description,
            options=product_detail.info,
            category_name=CATEGORY_INFO.name,
            category_id=CATEGORY_INFO.category_id,
            store_name=STORE_INFO.name,
            store_id=STORE_INFO.id,
            query=STORE_INFO.query
        )