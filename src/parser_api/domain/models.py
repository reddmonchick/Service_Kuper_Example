from enum import Enum

class CommandTypes(str, Enum):
    ALL_UPDATE = "all_update"
    UPDATE_LIST_ID = "update_list_id"
    SEARCH_REQUEST = "search_request"