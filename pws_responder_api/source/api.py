# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_restful import Api

from resources.resources_loader import Resources

logger = logging.getLogger(__name__)


def create_app():
    logger.info("Creating APP")

    app = Flask(__name__)
    api = Api(app)

    Resources.load_resources(api)

    return app


