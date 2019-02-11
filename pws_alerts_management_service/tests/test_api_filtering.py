import pytest
import json

from tests.test_api import assert_alerts

from .fixtures import AlertFactory2DB


# WARN: If a test fails, the nexts texts will also fail. It seems a problem with the db session.

# NOTE: More tests available here: https://github.com/pyeve/eve-sqlalchemy/blob/master/eve_sqlalchemy/tests/sql.py

@pytest.mark.order1
def test_root(api_client):
    rv = api_client.get("/")
    assert rv.status_code == 200


def test_get_alert_filter_where_severity_equals_39(api_client, orm_client):
    AlertFactory2DB(title="ALERT_TEST_1", severity=68)
    alert2 = AlertFactory2DB(title="ALERT_TEST_2", severity=39)

    rv = api_client.get("/alerts/?where={\"severity\": 39}")
    items = json.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == 1
    assert_alerts(items[0], alert2)


def test_get_alert_filter_where_status_equals_10(api_client, orm_client):
    alert1 = AlertFactory2DB(title="ALERT_TEST_1", status=10)
    alert2 = AlertFactory2DB(title="ALERT_TEST_2", status=10)

    rv = api_client.get("/alerts/?where={\"status\": 10}")
    items = json.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == 2
    assert_alerts(items[0], alert1)
    assert_alerts(items[1], alert2)


def test_get_alert_filter_where_severity_greater_than_50(api_client, orm_client):
    alert1 = AlertFactory2DB(title="ALERT_TEST_1", severity=68)
    AlertFactory2DB(title="ALERT_TEST_2", severity=39)

    rv = api_client.get("/alerts/?where={\"severity\": \">50\"}")
    items = json.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == 1
    assert_alerts(items[0], alert1)


def test_get_alert_filter_where_number_greater_than_50_and_less_than_60(api_client, orm_client):
    alert1 = AlertFactory2DB(title="ALERT_TEST_1", severity=58)
    AlertFactory2DB(title="ALERT_TEST_2", severity=39)

    rv = api_client.get("/alerts/?where=severity>50 and severity<60")
    items = json.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == 1
    assert_alerts(items[0], alert1)


# Should be mark.xfail, but session is not doing a rollback when fail
@pytest.mark.skip(reason="This syntax is not working")
def test_get_alert_filter_where_number_greater_than_50_and_less_than_60_FAIL(api_client, orm_client):
    alert1 = AlertFactory2DB(title="ALERT_TEST_1", severity=58)
    AlertFactory2DB(title="ALERT_TEST_2", severity=39)

    # Not working: Follow https://github.com/pyeve/eve-sqlalchemy/issues/114
    rv = api_client.get("/alerts/?where={\"severity\": \">50 and <60\"}")
    items = json.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == 1
    assert_alerts(items[0], alert1)


def test_get_alert_filter_where_title_equals_alert_test_1(api_client, orm_client):
    alert1 = AlertFactory2DB(title="ALERT_TEST_1", severity=68)
    AlertFactory2DB(title="ALERT_TEST_2", severity=39)

    # Get alerts with title equals to ALERT_TEST
    rv = api_client.get("/alerts/?where={\"title\": \"ALERT_TEST_1\"}")
    items = json.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == 1
    assert_alerts(items[0], alert1)


def test_get_alert_filter_in_title_alert(api_client, orm_client):
    # Not working: Follow https://github.com/pyeve/eve-sqlalchemy/issues/171
    # Here it is a workaround with the old-style
    alert1 = AlertFactory2DB(title="ALERT_TEST_1")
    AlertFactory2DB(title="ALERT_TEST_2")

    # Get alerts with title equals to ALERT_TEST
    param = {
        "title": ['ALERT_TEST_1', 'ALERT_TEST_3']
    }
    url = "/alerts/?where=" + json.dumps(param)
    rv = api_client.get(url)
    items = json.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == 1
    assert_alerts(items[0], alert1)


# Should be mark.xfail, but session is not doing a rollback when fail
@pytest.mark.skip(reason="This syntax is not working")
def test_get_alert_filter_in_title_alert_FAIL(api_client, orm_client):
    # Here it is a workaround with the old-style
    alert1 = AlertFactory2DB(title="ALERT_TEST_1")
    AlertFactory2DB(title="ALERT_TEST_2")

    # Get alerts with title equals to ALERT_TEST
    param = {
        "title": "in(\"('ALERT_TEST_1', 'ALERT_TEST_3')\")"
    }
    url = "/alerts/?where=" + json.dumps(param)
    rv = api_client.get(url)
    items = json.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == 1
    assert_alerts(items[0], alert1)


def test_get_alert_filter_since_oct_2018(api_client, orm_client):
    alert1 = AlertFactory2DB(title="ALERT_TEST_1")

    # Get alerts generated since 17 Oct 2018
    rv = api_client.get("/alerts/?where=created_at> \"Mon, 17 Oct 2018 03:00:00 GMT\"")
    items = json.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == 1
    assert_alerts(items[0], alert1)


def test_get_alert_filter_since_oct_2019(api_client, orm_client):
    AlertFactory2DB(title="ALERT_TEST_1")

    # Get alerts generated since 17 Oct 2019
    rv = api_client.get("/alerts/?where=created_at> \"Mon, 17 Oct 2019 03:00:00 GMT\"")
    items = json.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == 0
