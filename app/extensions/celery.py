from celery import Celery, Task
from flask import Flask


class CeleryExt:
    def __init__(
        self,
        app: Flask | None = None,
    ) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> Celery:
        class FlaskTask(Task):
            def __call__(self, *args: object, **kwargs: object) -> object:
                with app.app_context():
                    return self.run(*args, **kwargs)

        self._app = app
        self._celery = Celery(self._app.name, task_cls=FlaskTask)
        self._celery.config_from_object(self._app.config["CELERY"])
        self._celery.set_default()
        self._app.extensions["celery"] = self._celery
        return self._celery
