from parser_api.application.parser_factory import ParserFactory
from parser_api.application.services import ParserService
from parser_api.schemas.request_models import ScraperShop
from parser_api.application.parser_registry import get_parser_class


class RegistryParserFactory(ParserFactory):
    def get_parser(self, shop: ScraperShop) -> ParserService:
        parser_class = get_parser_class(shop)
        return parser_class()