import os
import csv
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app, db
from app.models import Color, Element, Inventory, InventoryMinifigs, InventoryParts, InventorySets, Minifig, Part, PartCategory, PartRelationship, Set, Theme

app = create_app(os.getenv('FLASK_CONFIG', 'default'))

@app.cli.command()
def deploy():
    db.create_all()

@app.cli.command()
def import_data():
    with db.get_engine().connect() as conn:
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

        for csv_file in files:
            with open(csv_file, 'r', newline='', encoding='utf-8') as fp:
                reader = csv.DictReader(fp)

                table_name = os.path.splitext(os.path.basename(csv_file))[0]
                cols = ','.join(reader.fieldnames)
                values_keys = ','.join('?' * len(reader.fieldnames))

                print(f'Insterting data from {csv_file} in {table_name}')
                conn.execute('INSERT INTO {} ({}) VALUES ({})'.format(table_name, cols, values_keys), [tuple(item.values()) for item in reader])
