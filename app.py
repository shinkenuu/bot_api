from os import environ

from flask import Flask
from flask_restful import Api
from pymongo import MongoClient

from config import app_config


def init_app(config_name: str):
    app = Flask('bot_api')
    app.config.from_object(app_config[config_name])

    return app


def init_db(config_name: str):
    config = app_config[config_name]

    client = MongoClient(host=config.DB_HOST, port=config.DB_PORT, serverSelectionTimeoutMS=1)
    db = client[config.DB_NAME]

    # Check connection with MongoDB
    client.server_info()

    return db


db = init_db(config_name=environ.get('APP_CONFIG', 'test'))

app = init_app(config_name=environ.get('APP_CONFIG', 'test'))
api = Api(app)

from views import *

api.add_resource(BotList, '/bots')
api.add_resource(BotDetail, '/bots/<string:id>')
