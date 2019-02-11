from datetime import datetime

from eve.io.base import BaseJSONEncoder

from sqlalchemy.engine.url import URL
import shapely.geometry
from geoalchemy2 import WKTElement, WKBElement

from .models.common import wkb_to_geojson


def construct_db_uri(db_configuration):
    config = db_configuration.copy()
    config["username"] = config["user"]
    del config["user"]
    config["drivername"] = "postgres"
    return URL(**config)


class CustomJSONEncoder(BaseJSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            if obj.microsecond == 0:
                return int(obj.timestamp())
            else:
                return obj.timestamp()
        if isinstance(obj, WKTElement):
            return dict(shapely.geometry.mapping(obj))
        elif isinstance(obj, WKBElement):
            return dict(wkb_to_geojson(obj))

        return super(CustomJSONEncoder, self).default(obj)

def construct_alert_stream_doc(url):
    return {'paths': {
        url: {
            'get': {
                'summary': 'Subscription endpoint for Event Source SSE stream,'
                           ' to be notified of new alerts.',
                'produces': ["text/event-stream"],
                'responses': {'schema': {"type": "json", "$ref": "#/definitions/Alert"}}
            }}}}
