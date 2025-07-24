from dishka import Provider, Scope, provide
from parser_api.infrastructure.parsers.kuper.kuper_parser import KuperParser
from parser_api.infrastructure.parsers.ozon.ozon_parser import OzonParser
from parser_api.application.parsing_service import ParsingService
from parser_api.application.parser_factory import ParserFactory
from parser_api.infrastructure.factory.parser_factory import RegistryParserFactory

class AppProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self):
        super().__init__()
        self._factory = RegistryParserFactory()

    @provide
    def parser_factory(self) -> ParserFactory:
        return self._factory

    @provide
    def parsing_service(
        self,
        parser_factory: ParserFactory,
    ) -> ParsingService:
        return ParsingService(parser_factory=parser_factory)