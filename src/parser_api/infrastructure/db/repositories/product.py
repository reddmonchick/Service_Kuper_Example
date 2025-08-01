from sqlalchemy.ext.asyncio import AsyncSession

from parser_api.schemas.models import ProductDetailDTO
from parser_api.infrastructure.db.models import Product

from typing import List


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def add_many(self, products_dto: List[ProductDetailDTO], batch_size=1000):
        products = [
            Product.from_dto(product_dto)
            for product_dto in products_dto
        ]
        
        self.session.add_all(products)
        await self.session.flush(products)
            