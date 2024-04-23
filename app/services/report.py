import json
import typing as t

import pandas as pd


class ReportService:
    def _find_first_key(
        self, possible_values: t.Iterable[str], search_list: t.Iterable[str]
    ):
        for key in possible_values:
            if key in search_list:
                return key
        return None

    def generate_report(
        self,
        parts: pd.DataFrame,
        fig_parts: pd.DataFrame,
        elements: pd.DataFrame,  # noqa: ARG002
    ):
        count_keys = ["count", "current"]
        parts_count_key = self._find_first_key(count_keys, parts.columns)
        fig_parts_count_key = self._find_first_key(count_keys, fig_parts.columns)

        if parts_count_key is None:
            parts["count"] = 0
            parts_count_key = "count"

        if fig_parts_count_key is None:
            fig_parts["count"] = 0
            fig_parts_count_key = "count"

        # Calculate missing pieces
        parts["missing"] = parts["quantity"] - parts[parts_count_key]
        fig_parts["missing"] = fig_parts["quantity"] - fig_parts[fig_parts_count_key]

        parts_data = json.loads(parts.to_json(orient="table")).get("data", [])
        fig_parts_data = json.loads(fig_parts.to_json(orient="table")).get("data", [])

        return {"parts": parts_data, "fig_parts": fig_parts_data}
