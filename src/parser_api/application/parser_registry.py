

from typing import Type, Dict
from src.parser_api.application.parser_factory import ParserFactory
from src.parser_api.application.services import ParserService
from src.parser_api.schemas.request_models import ScraperShop

_parser_registry: Dict[ScraperShop, Type[ParserService]] = {}


def register_parser(shop: ScraperShop):
    def decorator(cls: Type[ParserService]):
        _parser_registry[shop] = cls
        return cls
    return decorator


def get_parser_class(shop: ScraperShop) -> Type[ParserService]:
    parser_class = _parser_registry.get(shop)
    if not parser_class:
        raise ValueError(f"Unsupported shop: {shop}")
    return parser_class