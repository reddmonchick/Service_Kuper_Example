from typing import List, Dict, Any
from src.parser_api.application.services import ParserService
from src.parser_api.schemas.models import StoreDTO, CategoryDTO
from src.parser_api.application.parser_registry import register_parser
from src.parser_api.schemas.request_models import ScraperShop
import tls_client

from src.parser_api.infrastructure.db.uow import UnitOfWork
from src.parser_api.infrastructure.db.repositories import ProductRepository


class OzonParser(ParserService):

    def __init__(self, uow: UnitOfWork, repository: ProductRepository):
        self.uow = uow
        self.repository = repository
    
    def parse_all_products(self):
        ...
    
    def update_product_list(self):
        ...

    async def search_products(self, *args, **kwargs):
        # This is a stub implementation
        return {"status": "OK", "items_count": 0, "result": []}