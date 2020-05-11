import os


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-might-never-guess'
    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "c:/GH/my_webapps/app/uploads"

    SESSION_COOKIE_SECURE = True
    FILE_UPLOAD = "c:/GH/my_webapps/app/uploads"
    FILES_ALLOWED = ["TXT", "CSV"]


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "c:/GH/my_webapps/app/uploads"

    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False
