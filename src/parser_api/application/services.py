from abc import ABC, abstractmethod
from typing import Dict, Any
from parser_api.schemas.models import CategoryDTO

class ParserService(ABC):
    @abstractmethod
    def parse_all_products(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def update_product_list(self, product_ids: list) -> Dict[str, Any]:
        ...

    @abstractmethod
    def search_products(self, query: str) -> Dict[str, Any]:
        ...