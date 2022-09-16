import os

import dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from minio import Minio

dotenv.load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ.get("FLASK_CONFIG"))
app.secret_key = os.environ.get("APP_SECRET_KEY")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# minio_client = Minio(app)
minio_client = Minio(endpoint=app.config.get("MINIO_ENDPOINT"),
                     access_key=app.config.get("MINIO_ACCESS_KEY"),
                     secret_key=app.config.get("MINIO_SECRET_KEY"),
                     secure=False)

from api.routes import *
from api.models import *  # Требуется для работы alembic