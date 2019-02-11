# -*- coding: utf-8 -*-
from core import database


class ApiRepository:

    @staticmethod
    def get_responses(category=None):
        return database.get_response_plans(category)

    @staticmethod
    def get_response(response_id):
        return database.get_response_plan(response_id)

    @staticmethod
    def get_response_external_id(response_external_id):
        return database.get_response_plan_external_id(response_external_id)

    @staticmethod
    def add_response(response):
        return database.insert_response_plan(response)

    @staticmethod
    def modify_response(response_id, response):
        return database.update_response_plan(response_id, response)

    @staticmethod
    def delete_response(response_id):
        return database.delete_response_plan(response_id)
