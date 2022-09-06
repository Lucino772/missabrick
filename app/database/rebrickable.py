import gzip
import os
import requests
import tempfile
import shutil

from app.database.sqlite import SQLiteCLI
from app.logging import get_logger

logger = get_logger(__name__)

_DATA_URLS = [
    'https://cdn.rebrickable.com/media/downloads/themes.csv.gz',
    'https://cdn.rebrickable.com/media/downloads/colors.csv.gz',
    'https://cdn.rebrickable.com/media/downloads/part_categories.csv.gz',
    'https://cdn.rebrickable.com/media/downloads/parts.csv.gz',
    'https://cdn.rebrickable.com/media/downloads/part_relationships.csv.gz',
    'https://cdn.rebrickable.com/media/downloads/elements.csv.gz',
    'https://cdn.rebrickable.com/media/downloads/sets.csv.gz',
    'https://cdn.rebrickable.com/media/downloads/minifigs.csv.gz',
    'https://cdn.rebrickable.com/media/downloads/inventories.csv.gz',
    'https://cdn.rebrickable.com/media/downloads/inventory_parts.csv.gz',
    'https://cdn.rebrickable.com/media/downloads/inventory_sets.csv.gz',
    'https://cdn.rebrickable.com/media/downloads/inventory_minifigs.csv.gz'
]

def _donwload_gzip_file(url: str, dest: str):
    response = requests.get(url, stream=True)
    with open(dest, 'wb') as dest_fp:
        with gzip.open(response.raw, 'rb') as data:
            dest_fp.write(data.read())

class RebrickableDownloads:

    def __init__(self, db_cli: SQLiteCLI, directory: str = None) -> None:
        self.__directory = directory
        self.__db_cli = db_cli
        if self.__directory is None:
            self.__directory = tempfile.mkdtemp()

    def __del__(self):
        if os.path.exists(self.__directory):
            shutil.rmtree(self.__directory)

    def _get_files_dest(self, url: str):
        return os.path.join(self.__directory, os.path.splitext(os.path.basename(url))[0])
    
    def download(self):
        for url in _DATA_URLS:
            filename = self._get_files_dest(url)
            _donwload_gzip_file(url, filename)
            logger.info('Downloaded file {} ({})'.format(filename, url))
    
    def import2db(self):
        for filename in map(self._get_files_dest, _DATA_URLS):
            table_name = os.path.splitext(os.path.basename(filename))[0]
            logger.info('Importing data from {} in {}'.format(filename, table_name))
            ecode, _ = self.__db_cli.import_csv(filename.replace('\\', '\/'), table_name)
            if ecode == 0:
                logger.info('Data successfully imported to {}'.format(table_name))
            else:
                logger.info('Failed to import data to {}'.format(table_name))
