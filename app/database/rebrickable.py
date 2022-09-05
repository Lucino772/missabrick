import gzip
import os
import requests
import tempfile
import shutil

from app.database.sqlite import SQLiteCLI

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
            print('Downloaded:', filename)
    
    def import2db(self):
        for filename in map(self._get_files_dest, _DATA_URLS):
            table_name = os.path.splitext(os.path.basename(filename))[0]
            print(f'Importing data from {filename} in {table_name}: ', end='', flush=True)
            ecode, _ = self.__db_cli.import_csv(filename.replace('\\', '\/'), table_name)
            if ecode == 0:
                print('OK')
            else:
                print('Failed')
