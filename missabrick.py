import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app, db, db_cli, rebrickable
from app.database import utils as db_utils

app = create_app(os.getenv('FLASK_CONFIG', 'default'))

@app.cli.command()
def deploy():    
    if not db_cli.check_installation():
        print('SQLite3 shell not found ! Data cannot be imported')
        exit(1)

    rebrickable.download()
    rebrickable.import2db()

    with db as conn:
        db_utils.execute_script('create_aggregate_table.sql', conn)
