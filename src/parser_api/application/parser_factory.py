from abc import ABC, abstractmethod
from parser_api.application.services import ParserService
from parser_api.schemas.request_models import ScraperShop


class ParserFactory(ABC):
    @abstractmethod
    def get_parser(self, shop: ScraperShop) -> ParserService:
        pass