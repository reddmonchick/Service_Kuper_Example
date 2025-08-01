from typing import List, Dict, Any
from parser_api.application.services import ParserService
from parser_api.schemas.models import StoreDTO, CategoryDTO
from parser_api.application.parser_registry import register_parser
from parser_api.schemas.request_models import ScraperShop
import tls_client

from parser_api.infrastructure.db.uow import UnitOfWork 
from parser_api.infrastructure.db.repositories import ProductRepository


class OzonParser(ParserService):

    def __init__(self, uow: UnitOfWork, repository: ProductRepository):
        self.uow = uow
        self.repository = repository
    
    def parse_all_products(self):
        ...
    
    def update_product_list(self):
        ...

    def search_products(self):
        ...