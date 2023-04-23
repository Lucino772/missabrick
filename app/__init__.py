from flask import Flask

from app.catalog import blueprint as catalog_bp
from app.extensions import compress, db, migrate, session
from app.login import blueprint as login_bp
from app.services import (
    colors_srv,
    elements_srv,
    inv_minifigs_srv,
    inv_parts_srv,
    inv_sets_srv,
    inventories_srv,
    mail_srv,
    minifigs_srv,
    parts_cats_srv,
    parts_rels_srv,
    parts_srv,
    sets_srv,
    themes_srv,
    users_srv,
)
from app.settings import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # Extensions
    db.init_app(app)
    compress.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)

    # Services
    users_srv.init_app(app, db)
    mail_srv.init_app(app)

    colors_srv.init_app(app, db)
    elements_srv.init_app(app, db)
    inventories_srv.init_app(app, db)
    inv_minifigs_srv.init_app(app, db)
    inv_parts_srv.init_app(app, db)
    inv_sets_srv.init_app(app, db)
    minifigs_srv.init_app(app, db)
    parts_rels_srv.init_app(app, db)
    parts_cats_srv.init_app(app, db)
    parts_srv.init_app(app, db)
    sets_srv.init_app(app, db)
    themes_srv.init_app(app, db)

    # Blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(catalog_bp)
    return app
