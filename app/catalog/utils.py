import os
from tempfile import NamedTemporaryFile, mkstemp

import pandas as pd
from flask import current_app
from werkzeug.datastructures import FileStorage


# Web
def stream_file_and_remove(filename: str, fd: int = None):
    open_path = filename if fd is None else fd

    with open(open_path, "rb", closefd=True) as fp:
        yield from fp

    os.remove(filename)


def send_temp_file(
    set_number: str,
    parts: pd.DataFrame,
    fig_parts: pd.DataFrame,
    elements: pd.DataFrame,
):
    fd, filename = mkstemp()
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        parts.to_excel(writer, sheet_name="parts", index=False)
        fig_parts.to_excel(writer, sheet_name="minifigs", index=False)
        elements.to_excel(writer, sheet_name="elements", index=False)

    nbytes = os.stat(filename).st_size
    return current_app.response_class(
        stream_file_and_remove(filename, fd),
        headers={
            "Content-Disposition": f"inline; filename={set_number}.xlsx",
            "Content-Length": nbytes,
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "filename": f"{set_number}.xlsx",
        },
    )


def read_uploaded_set_excel_file(file: FileStorage):
    dataframes = {}
    with NamedTemporaryFile() as fp:
        file.save(fp)

        dataframes = pd.read_excel(
            fp, sheet_name=["parts", "minifigs", "elements"]
        )

    parts_df = dataframes.get("parts", None)
    minifigs_parts_df = dataframes.get("minifigs", None)
    elements_df = dataframes.get("elements", None)

    return parts_df, minifigs_parts_df, elements_df
