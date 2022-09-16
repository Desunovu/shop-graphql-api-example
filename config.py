import os

from dotenv import load_dotenv

load_dotenv()

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    APP_DIR = app_dir

    # Minio
    MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT")
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
    PRODUCTS_BUCKET = os.environ.get("PRODUCTS_BUCKET")


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI')


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI')


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI')
