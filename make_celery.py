from app import create_app

flask_app = create_app()
flask_app.app_context().push()
celery_app = flask_app.extensions["celery"]
