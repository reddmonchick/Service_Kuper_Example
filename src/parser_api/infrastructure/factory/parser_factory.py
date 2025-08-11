from src.parser_api.application.parser_factory import ParserFactory
from src.parser_api.application.services import ParserService
from src.parser_api.schemas.request_models import ScraperShop
from typing import Dict


class RegistryParserFactory(ParserFactory):
    def __init__(self, parsers: Dict[ScraperShop, ParserService]):
        self._parsers = parsers

    def get_parser(self, shop: ScraperShop) -> ParserService:
        parser = self._parsers.get(shop)
        if not parser:
            raise ValueError(f"Parser for shop {shop} not configured.")
        return parser