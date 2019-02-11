# -*- coding: utf-8 -*-
from flask_cors import CORS
from configmanager import ConfigManager

from resources.api_handlers import ResponderHandler


class Resources:
    def init_cors(app):
        cors_resources = [r'/responder/*']

        CORS(app, resources=cors_resources,
             origins=ConfigManager().configuration["frontend_cors"]["urls"])

    @staticmethod
    def load_resources(api):
        api.add_resource(ResponderHandler.Responder, '/responder/',
                         strict_slashes=False)

