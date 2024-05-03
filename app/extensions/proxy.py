from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


class ProxyFixExt:
    def __init__(
        self,
        app: Flask | None = None,
    ) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        self._app = app

        proxy_cfg = self._app.config.get("PROXY", None)
        if proxy_cfg is None:
            return None

        self._app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=proxy_cfg.x_for,
            x_proto=proxy_cfg.x_proto,
            x_host=proxy_cfg.x_host,
            x_port=proxy_cfg.x_port,
            x_prefix=proxy_cfg.x_prefix,
        )
