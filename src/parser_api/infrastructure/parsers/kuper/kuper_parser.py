from src.parser_api.application.services import ParserService
from src.parser_api.schemas.models import StoreDTO, CategoryDTO, ProductDTO, ProductDetailDTO
from src.parser_api.application.parser_registry import register_parser
from src.parser_api.schemas.request_models import ScraperShop
from src.parser_api.infrastructure.parsers.kuper.utils.category_fetch import CategoryTreeParser
from src.parser_api.infrastructure.parsers.kuper.utils.helper import extract_product_info

from typing import List, Dict, Any
import logging

import asyncio
import logging
from async_tls_client.session.session import AsyncSession

from src.parser_api.application.services import ParserService
from src.parser_api.infrastructure.db.uow import UnitOfWork # <-- Ваш UoW
from src.parser_api.infrastructure.utils.concurrency_utils import run_concurrently
from src.parser_api.infrastructure.db.repositories import ProductRepository

logger = logging.getLogger(__name__)


class KuperParser(ParserService):
    
    def __init__(self, uow: UnitOfWork, repository: ProductRepository):
        self.session = AsyncSession(
            client_identifier="chrome_120",
            random_tls_extension_order=True
        )
        self.uow = uow
        self.repository = repository

    

    async def parse_all_products(self) -> List[ProductDetailDTO]:
        """Parse all products from Kuper API"""
        return {
            "status": "OK",
            "items_count": 1,
            "result": 'TEST'
        }

    async def update_product_list(self, product_ids: List[str]) -> List[ProductDetailDTO]:
        """Update product information by list of product IDs"""
        return {
            "status": "OK",
            "updated_count": 0,
            "updated_products": '0'
        }


    async def search_products(self, query: str) -> List[ProductDetailDTO]:
        """Search products by query string"""
        return {
            "status": "OK",
            "items_count": 0,
            "result": 0
        }