from flask.cli import AppGroup, with_appcontext

from app.cli.imports.rebrickable import import_data

data_cli = AppGroup("data")


@data_cli.command("load")
@with_appcontext
def load_data():
    import_data()
