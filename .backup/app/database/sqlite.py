import os
from subprocess import getstatusoutput

from app.logging import get_logger

logger = get_logger(__name__)

class SQLiteCLI:

    def __init__(self, database_uri: str) -> None:
        self.__database_uri = database_uri

    def check_installation(self):
        ec = getstatusoutput('sqlite3 -version')[0]
        if ec != 0:
            return False

        return True

    def _dotcmd(self, *cmds):
        cmd = ' '.join(['sqlite3', self.__database_uri, '-cmd'] + [ f'"{cmd}"' for cmd in cmds])
        logger.debug('Executing SQLite3 dot command: {}'.format(cmd))
        return getstatusoutput(cmd)

    def import_csv(self, file: str, table: str = None):
        if table is None:
            table  = os.path.splitext(os.path.basename(file))[0]

        return self._dotcmd('.mode csv', f'.import {file} {table}')
