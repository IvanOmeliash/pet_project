from typing import List, Any

class BaseService:
    def __init__(self):
        self._data = []
        self._id_counter = 1

    def get_all(self, skip: int = 0, limit: int = 10) -> List[Any]:
        return self._data[skip : skip + limit]

    def get_by_id(self, item_id: int):
        item = next((x for x in self._data if x.id == item_id), None)
        if not item:
            raise ValueError(f"Item with id {item_id} not found")
        return item