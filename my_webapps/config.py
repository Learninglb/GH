import os


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-might-never-guess'
    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    CLIENT_IMAGES = "c:/GH/my_webapps/app/static/client/img"
    CLIENT_FILES = "c:/GH/my_webapps/app/static/client/csv"
    CLIENT_DATS = "c:/GH/my_webapps/app/static/client/dat"

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    MAX_FILE_FILESIZE = 0.5 * 1024 * 1024
    MAX_IMAGE_FILESIZE = 0.5 * 1024 * 1024
    FILES_ALLOWED = ["TXT", "CSV"]
    IMAGES_ALLOWED = ["JPG", "GIF", "PNG"]
    FILE_UPLOAD = "c:/GH/my_webapps/app/static/csv/uploads"
    IMAGE_UPLOAD = "c:/GH/my_webapps/app/static/img/uploads"

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"


    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False
