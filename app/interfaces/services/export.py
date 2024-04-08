import typing as t

from app.interfaces.services.service import IService


class IExportService(IService):
    def export_parts(
        self, set_id: str, quantity: int = 1
    ) -> t.Tuple[int, str]: ...
