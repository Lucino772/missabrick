from app.interfaces.services.service import IService


class ISearchService(IService):
    def parse_query(self, query: str):
        ...

    def search(self, search: str, keywords: dict, current_page: int, page_size: int):
        ...

    def get_years(self):
        ...

    def get_themes(self):
        ...
