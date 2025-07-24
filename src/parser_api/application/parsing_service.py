from parser_api.domain.models import CommandTypes
from parser_api.application.services import ParserService as ParserInterface
from parser_api.application.parser_factory import ParserFactory
from parser_api.schemas.request_models import ScraperShop

class ParsingService:
    def __init__(self, parser_factory: ParserFactory):
        self.parser_factory = parser_factory

    def execute_command(self, command: str, data, shop: ScraperShop):
        parser = self.parser_factory.get_parser(shop)
        if command == CommandTypes.ALL_UPDATE:
            return parser.parse_all_products()
        elif command == CommandTypes.UPDATE_LIST_ID:
            return parser.update_product_list(data)
        elif command == CommandTypes.SEARCH_REQUEST:
            return parser.search_products(data)
        else:
            raise ValueError(f"Unknown command: {command}")