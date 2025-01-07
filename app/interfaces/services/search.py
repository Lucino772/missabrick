from typing import Any, Protocol

from flask_sqlalchemy.pagination import Pagination

from app.interfaces.services.service import IService


class ISearchService(IService, Protocol):
    def parse_query(self, query: str) -> tuple[dict[Any, Any], str]: ...

    def search(
        self, search: str, keywords: dict, current_page: int, page_size: int
    ) -> Pagination: ...

    def get_years(self) -> list[int]: ...

    def get_themes(self) -> list[str]: ...
