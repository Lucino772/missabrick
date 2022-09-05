import sqlite3
import os
from flask import current_app

def execute_script(file: str, conn: sqlite3.Connection, *fmtargs, **fmtkwargs):
    with current_app.open_resource(os.path.join('database/scripts', file), 'r') as fp:
        script_str = fp.read()

    formatted = script_str.format(*fmtargs, **fmtkwargs)
    return conn.executescript(formatted)

def execute_query(file: str, conn: sqlite3.Connection, parameters = None, many: bool = False):
    with current_app.open_resource(os.path.join('database/queries', file), 'r') as fp:
        query_str = fp.read()

    if parameters is None:
        parameters = tuple()

    if many:
        return conn.executemany(query_str, parameters)
    else:
        return conn.execute(query_str, parameters)
