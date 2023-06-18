from flask.cli import with_appcontext

from app.catalog import blueprint
from app.catalog.imports.rebrickable import import_data


@blueprint.cli.command("load")
@with_appcontext
def load_data():
    import_data()
