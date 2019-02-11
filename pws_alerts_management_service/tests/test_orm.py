import pytest
from geoalchemy2 import WKTElement

from alerts_api.database import ORMClient
from alerts_api.models import Alert
from .fixtures import AlertDictFactory


ALERT = AlertDictFactory(
    the_geom=WKTElement('POINT (42.70562793820589 2.439453125)', srid=4326), type=30,
    sub_type="some_alert", severity=10, status=10, title="title", description="description")


@pytest.mark.third
def test_insert_one_alert_and_clear_table(db_conf):
    """Insert one alert over an empty table. Clear table afterward."""
    client = ORMClient(**db_conf)  # TODO change name client ORM
    client.create_tables()

    assert Alert.query.count() == 0
    client.insert_alert(ALERT)
    assert Alert.query.count() == 1
    client.clear_alerts()
    assert Alert.query.count() == 0

    client.close()
