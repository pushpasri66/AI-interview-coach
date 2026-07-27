from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Central SQLAlchemy instance
db = SQLAlchemy()

# Central Flask-Migrate instance
migrate = Migrate()


def init_db(app):
    """Initializes SQLAlchemy database and Flask-Migrate extension with application."""
    db.init_app(app)
    migrate.init_app(app, db)
