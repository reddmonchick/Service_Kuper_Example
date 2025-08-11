

from dishka import Provider, Scope, provide
from typing import Dict

from src.parser_api.infrastructure.parsers.kuper.kuper_parser import KuperParser
from src.parser_api.infrastructure.parsers.ozon.ozon_parser import OzonParser
from src.parser_api.application.parsing_service import ParsingService
from src.parser_api.application.parser_factory import ParserFactory
from src.parser_api.infrastructure.factory.parser_factory import RegistryParserFactory
from src.parser_api.schemas.request_models import ScraperShop
from src.parser_api.application.services import ParserService
from src.parser_api.infrastructure.db.uow import UnitOfWork
from src.parser_api.infrastructure.db.repositories import ProductRepository
from src.parser_api.application.excel_service import ExcelProcessingService


class AppProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_kuper_parser(self, uow: UnitOfWork, repository: ProductRepository) -> KuperParser:
        return KuperParser(uow=uow, repository=repository)
    
    @provide
    def get_ozon_parser(self, uow: UnitOfWork, repository: ProductRepository) -> OzonParser:
        return OzonParser(uow=uow, repository=repository)
    
    @provide
    def get_excel_service(self) -> ExcelProcessingService:
        return ExcelProcessingService()

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
        excel_service: ExcelProcessingService
    ) -> ParsingService:
        return ParsingService(parser_factory=parser_factory, excel_service=excel_service)