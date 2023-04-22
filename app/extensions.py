from flask_compress import Compress
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
compress = Compress()
migrate = Migrate()
