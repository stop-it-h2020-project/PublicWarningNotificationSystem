from datetime import datetime, timezone

from sqlalchemy import Column as _
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TIMESTAMP, String
from sqlalchemy import func

import geoalchemy2
import shapely.geometry
from geoalchemy2.shape import to_shape
from cerberus import ValidationError


Base = declarative_base()
_WGS84_COORDINATE_SYSTEM = 4326
GEO_TYPE = geoalchemy2.Geometry(geometry_type='POINT',
                                srid=_WGS84_COORDINATE_SYSTEM)
DT_TYPE = TIMESTAMP(timezone=False)
RULE_ID_TYPE = String(64)


def utc_now(with_microseconds=True):
    """Returns the current UTC datetime, timezone aware with or withouth microseconds."""
    return datetime.now(tz=timezone.utc) if with_microseconds else \
        datetime.now(tz=timezone.utc).replace(microsecond=0)


def _validate_the_geom(geom):
    """Takes a GeoJSON Point and converts it to a WKT"""
    long, lat = geom["coordinates"]
    errors = ""
    if lat < -90 or lat > 90:
        errors += f"Latitude {long} is out of range"
    if long < -180 or long > 180:
        errors += f"Longitude {long} is out of range"
    if errors:
        raise ValidationError(errors)

    shape = shapely.geometry.shape(geom)
    wkt = geoalchemy2.WKTElement(str(shape), srid=_WGS84_COORDINATE_SYSTEM)
    return wkt


class CommonColumns(Base):
    __abstract__ = True
    created_at = _(DT_TYPE, default=utc_now)
    updated_at = _(DT_TYPE, default=utc_now, onupdate=utc_now)
    _etag = _(String(40))



def wkb_to_geojson(wkb):
    if wkb is None:
        return None
    wkt = to_shape(wkb)
    gj = shapely.geometry.mapping(wkt)
    gj["coordinates"] = list(gj["coordinates"])
    # tuple to list, useful for tests
    return gj
