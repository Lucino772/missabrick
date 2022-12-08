import sqlite3
import threading

from app.logging import get_logger

logger = get_logger(__name__)

class _LocalDB(threading.local):
    
    def __init__(self, conn: sqlite3.Connection = None) -> None:
        self.__conn = conn

    @property
    def current(self):
        return self.__conn

    @current.setter
    def current(self, conn: sqlite3.Connection):
        self.__conn = conn


class SQLiteDatabase:

    def __init__(self, database_uri: str) -> None:
        self.__database_uri = database_uri
        self.__connections = []

        self.__local_data = _LocalDB()

    def __del__(self):
        for conn in self.__connections:
            conn.close()

    def _new_local_connection(self):
        self._close_local_connection()

        conn = sqlite3.connect(self.__database_uri)
        conn.set_trace_callback(print)
        conn.row_factory = sqlite3.Row
        logger.debug('New SQLite3 connection to {}'.format(self.__database_uri))

        self.__connections.append(conn)
        self.__local_data.current = conn

        return conn

    def _close_local_connection(self):
        if self.__local_data.current is not None:
            logger.debug('Closed SQLite3 connection to {}'.format(self.__database_uri))
            self.__connections.remove(self.__local_data.current)
            self.__local_data.current.close()

        self.__local_data.current = None

    def __enter__(self):
        return self._new_local_connection()

    def __exit__(self, *args):
        self._close_local_connection()
