import os

class Config(object):
    SECRET_KEY= os.environ.get('SECRET_KEY') or 'you-might-never-guess'
    FILE_UPLOAD = "c:/GH/my_webapps/app/uploads"
    FILES_ALLOWED = ["TXT", "CSV"]