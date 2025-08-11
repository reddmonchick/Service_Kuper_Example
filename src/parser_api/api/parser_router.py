from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Response
from dishka.integrations.fastapi import DishkaRoute, FromDishka # <-- Изменено здесь!
import pandas as pd
import io

from src.parser_api.application.parsing_service import ParsingService
from src.parser_api.schemas.request_models import ParserRequest
from src.parser_api.schemas.request_models import ScraperShop, CommandEnum

import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/v1/parser", route_class=DishkaRoute)

@router.post("/")
async def handle_parser_command(
    request: ParserRequest,
    service: FromDishka[ParsingService],
):
    logger.info("Получен запрос: %s", request.model_dump())
    try:
        result = await service.execute_command( 
            command=request.command,
            data=request.data,
            shop=request.shop,
        )
        return {"success": True, "result": result}
    except Exception as e:
        logger.error("Ошибка при обработке запроса: %s", str(e), exc_info=True)
        return {"success": False, "error": str(e)}
    
@router.post("/process-excel/") 
async def handle_excel_command(
    file: UploadFile = File(...),
    command: str = Form(...),
    shop: ScraperShop = Form(...),
    service: FromDishka[ParsingService] = None,
):
    contents = await file.read()
    excel_file_like = io.BytesIO(contents)
    df_input = pd.read_excel(excel_file_like, header=None)
    if df_input.empty:
        raise HTTPException(status_code=400, detail="Excel файл пуст")
    product_ids = df_input.iloc[:, 0].dropna().astype(str).tolist()
    logger.debug(f"Извлечено {len(product_ids)} ID товаров")

    result_bytes = await service.execute_command( 
        command=command, 
        data={"product_ids": product_ids},
        shop=shop,
    )
    
    return Response(
        content=result_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=result_{file.filename}"}
    )
