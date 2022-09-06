import sqlite3
import os
from flask import current_app
from app.logging import get_logger

logger = get_logger(__name__)

def execute_script(file: str, conn: sqlite3.Connection, *fmtargs, **fmtkwargs):
    with current_app.open_resource(os.path.join('database/scripts', file), 'r') as fp:
        script_str = fp.read()

    formatted = script_str.format(*fmtargs, **fmtkwargs)
    logger.debug('Executing SQL script \'{}\' with: {} {}'.format(file, fmtargs, fmtkwargs))
    return conn.executescript(formatted)

def execute_query(file: str, conn: sqlite3.Connection, parameters = None, many: bool = False):
    with current_app.open_resource(os.path.join('database/queries', file), 'r') as fp:
        query_str = fp.read()

    if parameters is None:
        parameters = tuple()

    logger.debug('Executing SQL query \'{}\' with {}'.format(file, parameters))
    if many:
        return conn.executemany(query_str, parameters)
    else:
        return conn.execute(query_str, parameters)
