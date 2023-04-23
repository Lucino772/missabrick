import os
import shutil
import tempfile

from flask.cli import with_appcontext

from app.catalog import blueprint
from app.services import rebrickable_srv


@blueprint.cli.command("load")
@with_appcontext
def load_data():
    directory = ""
    try:
        directory = tempfile.mkdtemp()
        rebrickable_srv.imports(directory)
    finally:
        if os.path.exists(directory):
            shutil.rmtree(directory)
