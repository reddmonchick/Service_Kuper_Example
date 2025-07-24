from typing import List, Dict, Any
from parser_api.application.services import ParserService
from parser_api.schemas.models import StoreDTO, CategoryDTO
from parser_api.application.parser_registry import register_parser
from parser_api.schemas.request_models import ScraperShop
#from parser_api.infrastructure.utils.recursive_walker import RecursiveWalker
import tls_client

@register_parser(ScraperShop.ozon)
class OzonParser(ParserService):
    
    def get_stores(self):
        ...
    
    def update_product_list(self):
        ...

    def search_products(self):
        ...