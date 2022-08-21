import os

import dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from ariadne import ObjectType

dotenv.load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ.get("FLASK_CONFIG"))
app.secret_key = os.environ.get("APP_SECRET_KEY")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from api.routes import *
from api.models import *  # Требуется для работы alembic