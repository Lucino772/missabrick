from typing import Any, Protocol

import pandas as pd

from app.interfaces.services.service import IService


class IReportService(IService, Protocol):
    def generate_report(
        self,
        parts: pd.DataFrame,
        fig_parts: pd.DataFrame,
        elements: pd.DataFrame,
    ) -> dict[str, Any]: ...
