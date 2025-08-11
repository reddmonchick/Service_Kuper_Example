import pytest
from unittest.mock import MagicMock, AsyncMock

from src.parser_api.application.parsing_service import ParsingService
from src.parser_api.application.excel_service import ExcelProcessingService
from src.parser_api.application.parser_factory import ParserFactory
from src.parser_api.domain.models import CommandTypes
from src.parser_api.schemas.request_models import ScraperShop


@pytest.fixture
def mock_parser_factory():
    return MagicMock(spec=ParserFactory)

@pytest.fixture
def mock_excel_service():
    return MagicMock(spec=ExcelProcessingService)

@pytest.fixture
def parsing_service(mock_parser_factory, mock_excel_service):
    return ParsingService(
        parser_factory=mock_parser_factory,
        excel_service=mock_excel_service
    )

@pytest.mark.asyncio
async def test_execute_command_all_update(parsing_service, mock_parser_factory):
    """
    Tests that the 'all_update' command correctly calls the parser.
    """
    # Arrange
    mock_parser = AsyncMock()
    mock_parser_factory.get_parser.return_value = mock_parser
    shop = ScraperShop.KUPER
    command = CommandTypes.ALL_UPDATE

    # Act
    await parsing_service.execute_command(command=command, data=None, shop=shop)

    # Assert
    mock_parser_factory.get_parser.assert_called_once_with(shop)
    mock_parser.parse_all_products.assert_awaited_once()

@pytest.mark.asyncio
async def test_execute_command_search_request(parsing_service, mock_parser_factory):
    """
    Tests that the 'search_request' command correctly calls the parser.
    """
    # Arrange
    mock_parser = AsyncMock()
    mock_parser_factory.get_parser.return_value = mock_parser
    shop = ScraperShop.KUPER
    command = CommandTypes.SEARCH_REQUEST
    test_data = {"query": "test"}

    # Act
    await parsing_service.execute_command(command=command, data=test_data, shop=shop)

    # Assert
    mock_parser_factory.get_parser.assert_called_once_with(shop)
    mock_parser.search_products.assert_awaited_once_with(test_data["query"])

@pytest.mark.asyncio
async def test_execute_command_process_excel(parsing_service, mock_excel_service):
    """
    Tests that the 'process_excel' command correctly calls the excel service.
    """
    # Arrange
    mock_excel_service.process_product_ids = AsyncMock(return_value=b"excel_bytes")
    shop = ScraperShop.KUPER
    command = CommandTypes.PROCESS_EXCEL
    test_data = {"product_ids": ["123", "456"]}

    # Act
    result = await parsing_service.execute_command(command=command, data=test_data, shop=shop)

    # Assert
    mock_excel_service.process_product_ids.assert_awaited_once()
    assert result == b"excel_bytes"

@pytest.mark.asyncio
async def test_execute_command_unknown_raises_error(parsing_service):
    """
    Tests that an unknown command raises a ValueError.
    """
    # Arrange
    shop = ScraperShop.KUPER
    command = "UNKNOWN_COMMAND"

    # Act & Assert
    with pytest.raises(ValueError, match=f"Unknown command: {command}"):
        await parsing_service.execute_command(command=command, data=None, shop=shop)
