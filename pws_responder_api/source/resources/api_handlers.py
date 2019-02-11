import logging

from flask_restful import reqparse

from resources import Resource, Response

logger = logging.getLogger(__name__)

object_parser = reqparse.RequestParser()
object_parser.add_argument("data", type=dict)


class ResponderHandler:
    class Responder(Resource):
        def post(self):
            args = object_parser.parse_args()
            try:
                self.repository.execute_response(args["data"])
                return Response.success(args["data"])
            except (AttributeError, ValueError) as err:
                logger.error(err)
                return Response.error()
