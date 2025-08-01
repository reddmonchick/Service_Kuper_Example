# di.py

from dishka import Provider, Scope, provide
from typing import Dict

# Импорты ваших парсеров и зависимостей
from parser_api.infrastructure.parsers.kuper.kuper_parser import KuperParser
from parser_api.infrastructure.parsers.ozon.ozon_parser import OzonParser
from parser_api.application.parsing_service import ParsingService
from parser_api.application.parser_factory import ParserFactory
from parser_api.infrastructure.factory.parser_factory import RegistryParserFactory
from parser_api.schemas.request_models import ScraperShop
from parser_api.application.services import ParserService
from parser_api.infrastructure.db.uow import UnitOfWork
from parser_api.infrastructure.db.repositories import ProductRepository

class AppProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_kuper_parser(self, uow: UnitOfWork, repository: ProductRepository) -> KuperParser:
        return KuperParser(uow=uow, repository=repository)
    
    @provide
    def get_ozon_parser(self, uow: UnitOfWork, repository: ProductRepository) -> OzonParser:
        return OzonParser(uow=uow, repository=repository)

    @provide
    def parser_factory(
        self, 
        kuper: KuperParser, 
        ozon: OzonParser
    ) -> ParserFactory:
        parsers: Dict[ScraperShop, ParserService] = {
            ScraperShop.KUPER: kuper,
            ScraperShop.OZON: ozon,
        }
        return RegistryParserFactory(parsers=parsers)

    @provide
    def parsing_service(
        self,
        parser_factory: ParserFactory,
    ) -> ParsingService:
        return ParsingService(parser_factory=parser_factory)