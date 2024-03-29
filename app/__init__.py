import os
from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name.capitalize()}Config")

    return app