from flask_migrate import Migrate, migrate
from app import app, db

migrate = Migrate(app, db)