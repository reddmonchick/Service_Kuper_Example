from dishka import Provider, Scope, provide
from src.parser_api.infrastructure.db.repositories.product import ProductRepository


class RepositoriesProvider(Provider):
    scope=Scope.REQUEST

    product_repository = provide(ProductRepository)