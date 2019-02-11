import logging

from configmanager import ConfigManager
from flask import Flask
from flask_restful import Api

from core import database
from resources.resources_loader import Resources
from utils import construct_db_uri

logger = logging.getLogger(__name__)
db_config = ConfigManager().get_specific_configuration("database")

SQLALCHEMY_SETTINGS = {
    "DEBUG": False,
    "SQLALCHEMY_DATABASE_URI": construct_db_uri(db_config),
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}


def create_app(settings=SQLALCHEMY_SETTINGS):
    logger.info("Connecting to DB")

    app = Flask(__name__)
    api = Api(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = settings["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings["SQLALCHEMY_TRACK_MODIFICATIONS"]

    with app.app_context():
        database.init_db()

    Resources.load_resources(api)

    return app, database
