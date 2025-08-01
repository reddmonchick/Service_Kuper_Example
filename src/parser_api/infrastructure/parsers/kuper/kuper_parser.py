from parser_api.application.services import ParserService
from parser_api.schemas.models import StoreDTO, CategoryDTO, ProductDTO, ProductDetailDTO
from parser_api.application.parser_registry import register_parser
from parser_api.schemas.request_models import ScraperShop
from parser_api.infrastructure.parsers.kuper.utils.category_fetch import CategoryTreeParser
from parser_api.infrastructure.parsers.kuper.utils.helper import extract_product_info

from typing import List, Dict, Any
import logging

import asyncio
import logging
from async_tls_client.session.session import AsyncSession

from parser_api.application.services import ParserService
from parser_api.infrastructure.db.uow import UnitOfWork # <-- Ваш UoW
from parser_api.infrastructure.utils.concurrency_utils import run_concurrently 
from parser_api.infrastructure.db.repositories import ProductRepository

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
        ...

    async def update_product_list(self, product_ids: List[str]) -> List[ProductDetailDTO]:
        ...


    async def search_products(self, query: str) -> List[ProductDetailDTO]:
        ...