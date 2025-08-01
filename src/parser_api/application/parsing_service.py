from parser_api.domain.models import CommandTypes
from parser_api.application.services import ParserService as ParserInterface
from parser_api.application.parser_factory import ParserFactory
from parser_api.schemas.request_models import ScraperShop
from parser_api.schemas.models import ProductDetailDTO 
from parser_api.application.excel_service import ExcelProcessingService 

from fastapi import UploadFile

from typing import Optional, Dict, Any, List


class ParsingService:
    def __init__(self, parser_factory: ParserFactory):
        self.parser_factory = parser_factory

    async def _search_products_for_excel(self, query: str, shop: ScraperShop) -> List[ProductDetailDTO]:
        """
        Utils for ExcelService
        """
        parser = self.parser_factory.get_parser(shop)
        if not parser:
            raise ValueError(f"Scraper for shop {shop} not found.")
        

        search_result_dict = await parser.update_product_list(query) 
        
        if search_result_dict.get('status') != 'OK':
            return [] 
        
        result_list = search_result_dict.get('updated_products', [])
        
        return result_list 


    async def execute_command(self, command: str,
                              data: Optional[Dict[str, Any]],
                              shop: ScraperShop,
                              ):
        if command == CommandTypes.ALL_UPDATE:
            parser = self.parser_factory.get_parser(shop)
            return await parser.parse_all_products()
        elif command == CommandTypes.UPDATE_LIST_ID:
            parser = self.parser_factory.get_parser(shop)
            return await parser.update_product_list(data)
        elif command == CommandTypes.SEARCH_REQUEST:
            parser = self.parser_factory.get_parser(shop)
            return await parser.search_products(data)
        elif command == CommandTypes.PROCESS_EXCEL: 
            product_ids = data.get("product_ids", [])
            if not product_ids:
                raise ValueError("Product_ids required for command process_excel.")

            excel_service = ExcelProcessingService(self._search_products_for_excel) 
            

            result_excel_bytes = await excel_service.process_product_ids( 
                product_ids=product_ids,
                shop=shop
            )
            return result_excel_bytes # return bytes excel
        else:
            raise ValueError(f"Unknown command: {command}")
