from __future__ import annotations
from enum import Enum
from pydantic import BaseModel
from typing import List, Union, Optional, Dict, Any

class CommandEnum(str, Enum):
    all_update = "all_update"
    update_list_id = "update_list_id"
    search_request = "search_request"
    process_excel = "process_excel"

class ScraperShop(str, Enum):
    def __new__(cls, value):
        obj = str.__new__(cls, value.lower())
        obj._value_ = value.lower() 
        return obj

    KUPER = "kuper"
    OZON = "ozon"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member 
        try:
            return super()._missing_(value)
        except (AttributeError, ValueError):
            return None

from typing import Dict, Any

class ParserRequest(BaseModel):
    command: CommandEnum
    data: Optional[Dict[str, Any]] = None
    shop: ScraperShop

