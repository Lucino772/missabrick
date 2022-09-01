import os
import csv
import gzip
import requests
from dotenv import load_dotenv
from subprocess import getstatusoutput

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app, db
from app.models import Color, Element, Inventory, InventoryMinifigs, InventoryParts, InventorySets, Minifig, Part, PartCategory, PartRelationship, Set, Theme

app = create_app(os.getenv('FLASK_CONFIG', 'default'))

def _download_datasets():
    urls = [
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

    for url in urls:
        response = requests.get(url, stream=True)
        filename = os.path.splitext(os.path.basename(url))[0]
        print('Downloaded:', filename)

        with open(os.path.join('./datasets', filename), 'wb') as fp:
            with gzip.open(response.raw, 'rb') as data:
                fp.write(data.read())

@app.cli.command()
def deploy():
    db.create_all()
    

    database = 'test-dev.sqlite'
    ec = getstatusoutput('sqlite3 -version')[0]
    if ec != 0:
        print('SQLite3 shell not found ! Data cannot be imported')
        exit(1)

    # _download_datasets()

    files = [
        './datasets/colors.csv',
        './datasets/elements.csv',
        './datasets/inventories.csv',
        './datasets/inventory_minifigs.csv',
        './datasets/inventory_parts.csv',
        './datasets/inventory_sets.csv',
        './datasets/minifigs.csv',
        './datasets/part_categories.csv',
        './datasets/part_relationships.csv',
        './datasets/sets.csv',
        './datasets/themes.csv',
        './datasets/parts.csv'
    ]
    for filename in files:
        table_name = os.path.splitext(os.path.basename(filename))[0]
        print(f'Importing data from {filename} in {table_name}: ', end='', flush=True)
        ecode = getstatusoutput(f'sqlite3 {database} -cmd ".mode csv" ".import {filename} {table_name}"')[0]
        if ecode == 0:
            print('OK')
        else:
            print('Failed')

