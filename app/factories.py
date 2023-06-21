from flask import current_app, g
from werkzeug.local import LocalProxy

from app.interfaces.factory.service import IServiceFactory


def _get_service_factory() -> "IServiceFactory":
    if "service_factory" not in g:
        g.service_factory = current_app.service_factory_class()

    return g.service_factory


def teardown_service_factory(exception):
    g.pop("service_factory", None)


service_factory: "IServiceFactory" = LocalProxy(_get_service_factory)
