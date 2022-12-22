import pandas as pd
import tempfile
import os

from werkzeug.datastructures import FileStorage

def create_temp_set_excel_file(parts: pd.DataFrame, fig_parts: pd.DataFrame, elements: pd.DataFrame):
    fd, filename = tempfile.mkstemp()
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        parts.to_excel(writer, sheet_name='parts', index=False)
        fig_parts.to_excel(writer, sheet_name='minifigs', index=False)
        elements.to_excel(writer, sheet_name='elements', index=False)

    return fd, filename

def read_uploaded_set_excel_file(file: FileStorage):
    dataframes = {}
    with tempfile.NamedTemporaryFile() as fp:
        file.save(fp)

        dataframes = pd.read_excel(fp, sheet_name=["parts", "minifigs", "elements"])

    parts_df = dataframes.get('parts', None)
    minifigs_parts_df = dataframes.get('minifigs', None)
    elements_df = dataframes.get('elements', None)

    return parts_df, minifigs_parts_df, elements_df

def stream_file_and_remove(filename: str, fd: int = None):
    open_path = filename if fd is None else fd

    with open(open_path, 'rb', closefd=True) as fp:
        yield from fp
    
    os.remove(filename)
