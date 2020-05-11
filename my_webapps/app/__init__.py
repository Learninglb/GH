
from flask import Flask
from config import Config

app = Flask(__name__)
if app.config['ENV'] == 'production':
    app.config.from_object("config.ProductionConfig")
elif app.config['ENV'] == 'testing':
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

from app import admin_views
from app import views