import typing as t

from app.interfaces.services.service import IService

if t.TYPE_CHECKING:
    import pandas as pd


class IReportService(IService):
    def generate_report(
        self,
        parts: "pd.DataFrame",
        fig_parts: "pd.DataFrame",
        elements: "pd.DataFrame",
    ) -> t.Dict[str, t.Any]:
        ...
