import pytest
import fixtures
from source.user_defined_functions.queue_sender.alert_definition import AlertDefinition

@pytest.mark.parametrize("item_type", ["tiltmeter"])
def test_alert_definitions(item_type, alert_definition):
    alert = alert_definition
    alert["alert"]["description"] = ""
    assert alert == fixtures.EXPECTED_ALERT

@pytest.fixture(scope="function")
def alert_definition(item_type):
    options = fixtures.create_options(item_type)
    point = fixtures.generate_point(item_type)
    definition = AlertDefinition(options)
    return definition.get_alert(point)
