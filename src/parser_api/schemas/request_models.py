from __future__ import annotations
from enum import Enum
from pydantic import BaseModel
from typing import List, Union, Optional

class CommandEnum(str, Enum):
    all_update = "all_update"
    update_list_id = "update_list_id"
    search_request = "search_request"

class ScraperShop(str, Enum):
    kuper = 'Kuper'
    ozon = 'Ozon'

class ParserRequest(BaseModel):
    command: CommandEnum
    data: Optional[Union[str, List[str]]] = None
    shop: ScraperShop

