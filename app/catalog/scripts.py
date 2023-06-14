import os
import shutil
import tempfile

from flask.cli import with_appcontext

from app.catalog import blueprint
from app.services.importer import importer_service


@blueprint.cli.command("load")
@with_appcontext
def load_data():
    directory = ""
    try:
        directory = tempfile.mkdtemp()
        importer_service.imports(directory)
    finally:
        if os.path.exists(directory):
            shutil.rmtree(directory)
