from abc import ABC, abstractmethod
from src.parser_api.application.services import ParserService
from src.parser_api.schemas.request_models import ScraperShop


class ParserFactory(ABC):
    @abstractmethod
    def get_parser(self, shop: ScraperShop) -> ParserService:
        pass