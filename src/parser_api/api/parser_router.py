from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from parser_api.application.parsing_service import ParsingService
from parser_api.schemas.request_models import ParserRequest
#from parser_api.schemas.response_models import ParserResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/parser", route_class=DishkaSyncRoute)

@router.post("/")
async def handle_parser_command(
    request: ParserRequest,
    service: FromDishka[ParsingService],
):
    logger.info("Получен запрос: %s", request.model_dump())  # Логируем входящий запрос
    try:
        result = service.execute_command(
            command=request.command,
            data=request.data,
            shop=request.shop,
        )
        logger.info("Запрос обработан успешно")  # Логируем успешный результат
        return {"success": True, "result": result}
    except Exception as e:
        logger.error("Ошибка при обработке запроса: %s", str(e), exc_info=True)  # Логируем ошибки
        return {"success": False, "error": str(e)}