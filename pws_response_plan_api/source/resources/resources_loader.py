# -*- coding: utf-8 -*-
from flask_cors import CORS
from configmanager import ConfigManager

from resources.api_handlers import ResponsePlanHandler


class Resources:
    def init_cors(app):
        cors_origins = ConfigManager().configuration["frontend_cors"]["urls"]

        CORS(app, resources=r'/response-plans/*', origins=cors_origins)

    @staticmethod
    def load_resources(api):
        api.add_resource(ResponsePlanHandler.ResponsePlansFilter,
                         '/response-plans/alert-category/<string:alert_category>',
                         strict_slashes=False)

        api.add_resource(ResponsePlanHandler.ResponsePlans, '/response-plans',
                         strict_slashes=False)

        api.add_resource(ResponsePlanHandler.ResponsePlan, '/response-plans/<string:response_id>',
                         strict_slashes=False)
