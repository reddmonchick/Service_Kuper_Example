from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from src.parser_api.schemas.models import ProductDetailDTO
from src.parser_api.infrastructure.db.models import Product

from typing import List


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def add_many(self, products_dto: List[ProductDetailDTO]):
        """
        Adds or updates multiple products in the database using an "upsert" operation.
        If a product with the same ID already exists, it updates the record.
        """
        if not products_dto:
            return

        # Manually construct dictionaries from DTOs, mirroring the logic in Product.from_dto
        products_data = []
        for product_detail in products_dto:
            basic_info = product_detail.basic_info
            category_info = product_detail.category
            store_info = product_detail.category.store
            products_data.append({
                "id": basic_info.id,
                "name": basic_info.name,
                "photos": basic_info.photos,
                "price_basic": basic_info.price_basic,
                "price_with_discount": basic_info.price_with_discount,
                "discount_size": basic_info.discount_size,
                "quantity_rate": product_detail.quantity_rate,
                "description": product_detail.description,
                "options": product_detail.info,
                "category_name": category_info.name,
                "category_id": category_info.category_id,
                "store_name": store_info.name,
                "store_id": store_info.id,
                "query": store_info.query
            })

        # Create an insert statement with an ON CONFLICT clause for "upsert"
        stmt = insert(Product).values(products_data)
        
        # Define which columns to update in case of a conflict
        update_dict = {
            c.name: c
            for c in stmt.excluded
            if c.name != 'id' # Don't update the ID itself
        }

        stmt = stmt.on_conflict_do_update(
            index_elements=['id'], # The column that causes the conflict
            set_=update_dict
        )

        # Execute the upsert statement and commit
        await self.session.execute(stmt)
        await self.session.commit()
