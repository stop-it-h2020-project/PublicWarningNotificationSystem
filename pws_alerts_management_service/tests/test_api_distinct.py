import pytest
import json

from .fixtures import AlertFactory2DB


@pytest.mark.parametrize("field, test_input,expected", [
    ("type", [{"type": 10}, {"type": 10}], [10]),
    ("type", [{"type": 10}, {"type": 20}], [10, 20]),
    ("type", [{"type": 10}, {"type": 10}, {"type": 20}], [10, 20]),
    ("title", [{"type": 10, "title": "name1"}, {"type": 10, "title": "name2"}], ["name1", "name2"]),
    ("severity", [{"type": 10, "severity": 1}, {"type": 20, "severity": 1}], [1])
])
def test_get_alert_filter_in_title_alert(api_client, orm_client, field, test_input, expected):
    for alert in test_input:
        AlertFactory2DB(**alert)

    url = f"/alerts/distinct/{field}"
    rv = api_client.get(url)
    items = json.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == len(expected)
    assert items.sort() == expected.sort()
