
import pandas as pd
import io

import logging
from datetime import datetime
from typing import List, Callable, Any

from src.parser_api.schemas.request_models import ScraperShop
from src.parser_api.schemas.models import ProductDetailDTO


logger = logging.getLogger(__name__)

class ExcelProcessingService:
    def __init__(self):
        pass


    async def process_product_ids(self, search_function: Callable[[str, ScraperShop], List[ProductDetailDTO]], product_ids: List[str], shop: ScraperShop) -> bytes:
        """
        Fetch couple of ids, and write it into the excel file
        """
        logger.info(f"Start excel proccesing  {len(product_ids)} ID product for store {shop}")
        results_for_excel = []
        for product_id_str in product_ids:
            try:
                 product_id = int(product_id_str) 
            except ValueError:
                 logger.warning(f"Incorrect ID '{product_id_str}', skip.")
                 results_for_excel.append({"product_id": product_id, "status": "Не найден"})
                 continue

            try:
                
                search_result: List[ProductDetailDTO] = await search_function([str(product_id)], shop)
                
                if not search_result:
                      results_for_excel.append({"product_id": product_id,
                                                "status": "Не найден"})
                      logger.info(f'Not found any result about {product_id} {search_result}')
                      continue

                available_products = [p for p in search_result if p.basic_info and p.quantity_rate and p.basic_info.price_with_discount]
                if not available_products:
                      results_for_excel.append({"product_id": product_id,
                                                "status": "Нет в наличии"})
                      logger.info(f'Product unavailable, skip  {product_id}')
                      continue

                cheapest_product_detail = min(available_products, key=lambda p: p.basic_info.price_with_discount)
                cheapest_product = cheapest_product_detail.basic_info
                cheapest_store = cheapest_product_detail.category.store 

                total_metro_lenta = sum(
                     p.quantity_rate 
                     for p in search_result 
                     if p.basic_info and p.quantity_rate and 
                        any(name in (p.category.store.name if p.category.store.name else '') for name in ['METRO', 'Лента'])
                 )
                
                quantity_metro = sum(p.quantity_rate for p in search_result
                                     if p.basic_info and p.quantity_rate and p.category.store.name == 'METRO')
                price_metro = sum(p.basic_info.price_with_discount for p in search_result
                                     if p.basic_info and p.quantity_rate and p.category.store.name == 'METRO')

                results_for_excel.append({
                    "product_id": product_id,
                    "status": "найден",
                    "cheapest_store_name": cheapest_store.name if cheapest_store.name else "Неизвестно",
                    "cheapest_price": cheapest_product.price_with_discount,
                    "cheapest_quantity": cheapest_product_detail.quantity_rate,
                    "total_quantity_metro_lenta": total_metro_lenta or 0,
                    "quantity_metro": quantity_metro,
                    "price_metro": price_metro,
                    "last_update_date": datetime.now(),
                 })
                #logger.debug(f'excel results {results_for_excel}')

            except Exception as e:
                 logger.error(f"Error when fetch ID {product_id_str}: {e}")
                 results_for_excel.append({...})
                 continue

        # --- Create excel file ---
        df_output = pd.DataFrame(results_for_excel)
        output = io.BytesIO()
        try:
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_output.to_excel(writer, index=False, sheet_name='Результаты')
            output.seek(0)
            logger.info("Proccesing excel file and create")
            return output.read()
        except Exception as e:
            logger.error(f"Error when create excel file: {e}")
            raise ValueError(f"Error when create excel file: {e}")
