import pytest
import io
import pandas as pd
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from dishka import make_async_container, Provider, provide, Scope

# Import the factory function, not the global app instance
from parser_api.main import create_app, ConfigProvider, DatabaseProvider, RepositoriesProvider, FastapiProvider
from parser_api.application.parsing_service import ParsingService
from parser_api.schemas.request_models import ScraperShop, CommandEnum

# This mock will be used across tests
mock_parsing_service = AsyncMock(spec=ParsingService)

# A custom provider for our tests that provides the mock service
class TestAppProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_service(self) -> ParsingService:
        return mock_parsing_service

@pytest.fixture
def client():
    """
    This fixture creates a new FastAPI app and a TestClient for each test.
    It configures a test-specific DI container with a mocked ParsingService.
    """
    # Reset the mock's state before each test run
    mock_parsing_service.reset_mock()

    # Create a DI container for testing, swapping the real AppProvider
    # with our TestAppProvider.
    container = make_async_container(
        TestAppProvider(),
        ConfigProvider(),
        DatabaseProvider(),
        RepositoriesProvider(),
        FastapiProvider()
    )

    # Create a fresh app instance using the test container
    app = create_app(container)

    # Yield a client to run requests against the test app
    with TestClient(app) as test_client:
        yield test_client

    # The container will be closed by the app's lifespan manager

def test_process_excel_command(client):
    """
    Tests the /process-excel/ endpoint with a mocked service.
    """
    # Arrange
    mock_parsing_service.execute_command.return_value = b"excel_file_bytes"

    df = pd.DataFrame({'product_id': [101, 102, 103]})
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, header=False)
    excel_buffer.seek(0)

    files = {'file': ('test_products.xlsx', excel_buffer, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    data = {
        'command': CommandEnum.process_excel.value,
        'shop': ScraperShop.KUPER.value
    }

    # Act
    response = client.post("/api/v1/parser/process-excel/", files=files, data=data)

    # Assert
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    assert response.content == b"excel_file_bytes"

    mock_parsing_service.execute_command.assert_awaited_once_with(
        command=CommandEnum.process_excel.value,
        data={"product_ids": ['101', '102', '103']},
        shop=ScraperShop.KUPER
    )

def test_generic_parser_command(client):
    """
    Tests the generic "/" endpoint with a mocked service.
    """
    # Arrange
    mock_execute_result = {"status": "OK", "items_count": 1}
    mock_parsing_service.execute_command.return_value = mock_execute_result

    request_payload = {
        "command": CommandEnum.search_request.value,
        "shop": ScraperShop.OZON.value,
        "data": {"query": "some product"}
    }

    # Act
    response = client.post("/api/v1/parser/", json=request_payload)

    # Assert
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["success"] is True
    assert response_json["result"] == mock_execute_result

    mock_parsing_service.execute_command.assert_awaited_once_with(
        command=CommandEnum.search_request.value,
        data={"query": "some product"},
        shop=ScraperShop.OZON
    )
