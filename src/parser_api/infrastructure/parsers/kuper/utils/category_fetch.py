from typing import List, Dict, Optional
from src.parser_api.schemas.models import CategoryDTO, StoreDTO


class CategoryTreeParser:
    def __init__(self, raw_data: List[Dict], store: StoreDTO):
        self.raw_data = raw_data
        self.store = store
        self.leaf_dto_list: List[CategoryDTO] = []

    def _is_leaf(self, node: Dict) -> bool:
        return not node.get("children")

    def _traverse(self, node: Dict, path: List[str] = None):
        if path is None:
            path = []

        current_path = path + [node["name"]]

        if self._is_leaf(node):
            dto = CategoryDTO(
                category_id=node["id"],
                store = self.store,
                name=node["name"],
                path=" > ".join(current_path)
            )
            self.leaf_dto_list.append(dto)
        else:
            for child in node.get("children", []):
                self._traverse(child, current_path)

    def walk(self) -> List[CategoryDTO]:
        for root_category in self.raw_data:
            self._traverse(root_category)
        return self.leaf_dto_list