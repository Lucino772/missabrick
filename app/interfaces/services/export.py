from typing import Protocol

from app.interfaces.services.service import IService


class IExportService(IService, Protocol):
    def export_parts(self, set_id: str, quantity: int = 1) -> tuple[int, str]: ...
