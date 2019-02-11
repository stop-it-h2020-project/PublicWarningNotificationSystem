import pytest

# Trick needed in order to prevent conflict with requests.post() argument "json" when using it in monkeypatch
import json as json_lib

from datetime import datetime
import requests
import uuid

from pws_common import enums

from alerts_api.models import Alert, ALERT_RESOLVED_STATUS
from alerts_api.models.common import wkb_to_geojson
from alerts_api.api import RECURRENCE_MESSAGE

from .fixtures import point_factory, AlertFactory2DB, AlertDictFactory, RuleFactory2DB, \
    automatic_response, manual_response


@pytest.mark.order1
def test_root_endpoint(api_client):
    rv = api_client.get("/")
    assert rv.status_code == 200


def test_alert_missing(api_client):
    rv = api_client.get("/alerts/notvalid")
    assert rv.status_code == 404


def test_retrieve_alert(api_client, orm_client):
    alert_id = 123
    coordinates = point_factory(42.254611, 1.141365)

    assert orm_client.session.query(Alert).count() == 0
    alert_1 = AlertFactory2DB(id=alert_id, the_geom=coordinates)
    assert orm_client.session.query(Alert).count() == 1

    rv = api_client.get(f"/alerts/{alert_id}")

    assert rv.status_code == 200
    response_content = json_lib.loads(rv.data)
    assert "created_at" in response_content
    assert "updated_at" in response_content
    assert response_content["created_at"] == pytest.approx(response_content["updated_at"], abs=0.001), \
        "created_at should be approximatelly the same that updated_at, a difference of microseconds"

    assert response_content["created_at"] == pytest.approx(datetime.utcnow().timestamp(), 0.001), \
        "created_at should be very close to the current UTC time."

    assert_alerts(response_content, alert_1)


def test_retrieve_collection_alerts(api_client, orm_client):
    inserted2 = AlertFactory2DB(the_geom=point_factory(42.254611, 1.141365))
    inserted3 = AlertFactory2DB(the_geom=point_factory(42.380932, 2.141365))

    rv = api_client.get("/alerts/")
    items = json_lib.loads(rv.data)["_items"]
    assert rv.status_code == 200
    assert len(items) == 2
    assert_alerts(items[0], inserted2)
    assert_alerts(items[1], inserted3)


def test_post_alert(api_client, orm_client):
    alert = AlertDictFactory(the_geom=point_factory(42.56, 2.78), meta_type="meta_data",
        severity=68, status=10,
        description='Axis one of tiltmeter exceeded [1] '
                    'degree threshold during more than 2 minutes')

    rv = api_client.post("/alerts/", data=json_lib.dumps(alert),
        content_type='application/json')

    assert rv.status_code == 201
    response = json_lib.loads(rv.data)

    inserted = orm_client.session.query(Alert).get(response["id"])
    assert_alerts(alert, inserted)


def test_fails_post_alert_for_id(api_client, clear_tables):
    alert_4 = AlertDictFactory()
    alert_4["id"] = 4
    rv = api_client.post("/alerts/", data=json_lib.dumps(alert_4),
        content_type='application/json')
    assert rv.status_code == 422
    response = json_lib.loads(rv.data)
    assert response["_error"]["message"] == "\'id\' field is not allowed."


def test_fails_post_alert_for_rule(api_client, clear_tables):
    rule_id = "#BATMAN"
    RuleFactory2DB(id=rule_id)
    alert = AlertDictFactory(rule=rule_id)

    rv = api_client.post("/alerts/", data=json_lib.dumps(alert),
        content_type='application/json')
    assert rv.status_code == 422
    response = json_lib.loads(rv.data)
    assert response["_error"]["message"] == "\'rule\' field is not allowed. Use \'rule_id\'."


def test_post_two_same_rule(api_client, orm_client):
    """Test whether is possible to insert multiple alerts for the same rule
    and if the [de]serialization is made using rule_id."""

    rule_id = "rule_11"
    RuleFactory2DB(id=rule_id)
    a1 = AlertDictFactory(rule_id=rule_id)
    a1["related_item_id"] = "4444"
    a2 = AlertDictFactory(rule_id=rule_id)
    a2["related_item_id"] = "9999"

    # POST one alert
    r = api_client.post("/alerts/", data=json_lib.dumps(a1), content_type='application/json')
    assert r.status_code == 201
    # POST another alert
    r2 = api_client.post("/alerts/", data=json_lib.dumps(a2), content_type='application/json')
    assert r2.status_code == 201

    # GET the second alert
    alerts = orm_client.session.query(Alert).all()
    r3 = api_client.get(f"/alerts/{alerts[1].id}", )
    response = (json_lib.loads(r3.data))

    assert "rule" not in response
    assert len(alerts) == 2
    for alert in alerts:
        assert alert.rule_id == rule_id


def test_change_alert_status(api_client, orm_client):
    rule_id = "que_rule"
    RuleFactory2DB(id=rule_id)
    a = AlertDictFactory(rule_id=rule_id)
    old_status = a["status"]

    # POST one alert
    r1 = api_client.post("/alerts/", data=json_lib.dumps(a), content_type='application/json')
    assert r1.status_code == 201

    # Get the data from the posted alert
    data = json_lib.loads(r1.data)
    alert_id = data["id"]

    r2 = api_client.get(f"/alerts/{alert_id}")
    data = json_lib.loads(r2.data)
    etag = data["_etag"]

    assert old_status == data["status"]

    # Set new status != old one
    new_status = old_status + 10

    r3 = api_client.patch(f"/alerts/{alert_id}",
        headers={"If-Match": etag, "Content-Type": "application/json"},
        data=json_lib.dumps({"status": new_status}))

    assert r3.status_code == 200

    # Ensure status was changed
    r4 = api_client.get(f"/alerts/{alert_id}")

    assert json_lib.loads(r4.data)["status"] == new_status


def test_resolve_alert(api_client, orm_client):
    """Change alert status to RESOLVED and check the timestamp changes too."""

    a = AlertFactory2DB(operative_status=ALERT_RESOLVED_STATUS - 1)
    alert_id = a.id
    assert a.resolved_at is None
    etag = json_lib.loads(api_client.get(f"/alerts/{alert_id}").data)["_etag"]

    res = api_client.patch(f"/alerts/{alert_id}",
        headers={"If-Match": etag, "Content-Type": "application/json"},
        data=json_lib.dumps({"operative_status": ALERT_RESOLVED_STATUS}))

    assert res.status_code == 200, print(res.data)
    resolved_ts = json_lib.loads(api_client.get(f"/alerts/{alert_id}").data)["resolved_at"]
    assert resolved_ts == pytest.approx(datetime.utcnow().timestamp(), abs=0.1)  # 0.1 seconds


def test_fails_post_alert_for_repeated(api_client, orm_client):
    rule_id = "que_rule_rule"
    RuleFactory2DB(id=rule_id)
    a1 = AlertDictFactory(rule_id=rule_id)
    a2 = AlertDictFactory(rule_id=rule_id)

    # POST one alert
    r1 = api_client.post("/alerts/", data=json_lib.dumps(a1), content_type='application/json')
    assert r1.status_code == 201

    response1 = json_lib.loads(r1.data)
    inserted1 = orm_client.session.query(Alert).get(response1["id"])
    assert inserted1.recurrence == 1

    # Tries to insert same alert several times, none will be, recurrence increases
    for i in range(2, 5):
        # POST another alert
        r2 = api_client.post("/alerts/", data=json_lib.dumps(a2), content_type='application/json')

        # Ensure insert rejected
        assert r2.status_code == 422
        response2 = json_lib.loads(r2.data)
        assert response2["_error"]["message"] == RECURRENCE_MESSAGE

        # Ensure recurrence is increased
        recurrence = json_lib.loads(api_client.get("/alerts/{}".format(
            response1["id"])).data)["recurrence"]
        assert recurrence == i


@pytest.mark.parametrize("forward_ok, automatic_response_plan_found, response_ok, result",
    [
        (True, True, True, enums.Status.FORWARDED | enums.Status.AUTOMATIC_RESPONSE_PLAN_EXECUTED),
        (True, True, False, enums.Status.FORWARDED),
        (False, True, True, enums.Status.AUTOMATIC_RESPONSE_PLAN_EXECUTED),
        (False, True, False, enums.Status.NO_ACTION),
        (True, False, None, enums.Status.FORWARDED),
        (False, False, None, enums.Status.NO_ACTION)
    ]
)
def test_on_confirm(api_client, orm_client, forward_ok, automatic_response_plan_found, response_ok, result, monkeypatch):
    def fake_api_post(alert_api_url, json):  # TODO: prevent duplicated code
        class FakeResponse(object):
            def __init__(self):
                if json.get("data", None):     # Call to the responder api
                    self.ok = response_ok
                else:
                    self.ok = forward_ok        # Call to the external alerts module api
            def raise_for_status(self):
                raise Exception
        return FakeResponse()
    monkeypatch.setattr(requests, "post", fake_api_post)

    def fake_response_plan_api_get(alert_api_url):
        class FakeResponse(object):
            def __init__(self):
                self.ok = True
                if automatic_response_plan_found:
                    self.text = json_lib.dumps(automatic_response)
                else:
                    self.text = json_lib.dumps(manual_response)

        return FakeResponse()
    monkeypatch.setattr(requests, "get", fake_response_plan_api_get)

    rule_id = str(uuid.uuid4())
    RuleFactory2DB(id=rule_id)
    a = AlertDictFactory(rule_id=rule_id)
    old_operative_status = a["operative_status"]
    old_status = a["status"]

    # POST one alert
    r1 = api_client.post("/alerts/", data=json_lib.dumps(a), content_type='application/json')
    assert r1.status_code == 201

    # Get the data from the posted alert
    data = json_lib.loads(r1.data)
    alert_id = data["id"]

    r2 = api_client.get(f"/alerts/{alert_id}")
    data = json_lib.loads(r2.data)
    etag = data["_etag"]

    assert old_operative_status == data["operative_status"]
    assert old_status == data["status"]

    # Set new operative_status != old one, but still not corresponding to the status of confirmed alerts
    new_operative_status = enums.OperativeStatus.SEEN

    r3 = api_client.patch(f"/alerts/{alert_id}",
        headers={"If-Match": etag, "Content-Type": "application/json"},
        data=json_lib.dumps({"operative_status": new_operative_status}))

    assert r3.status_code == 200

    # Ensure status was changed
    r4 = api_client.get(f"/alerts/{alert_id}")
    data = json_lib.loads(r4.data)
    etag = data["_etag"]

    assert json_lib.loads(r4.data)["operative_status"] == new_operative_status
    assert json_lib.loads(r4.data)["status"] == old_status

    # Set new operative_status != old one, AND corresponding to the status of confirmed alerts
    new_operative_status = enums.OperativeStatus.CONFIRMED

    r4 = api_client.patch(f"/alerts/{alert_id}",
        headers={"If-Match": etag, "Content-Type": "application/json"},
        data=json_lib.dumps({"operative_status": new_operative_status}))

    assert r4.status_code == 200

    # Ensure status was changed
    r5 = api_client.get(f"/alerts/{alert_id}")

    assert json_lib.loads(r5.data)["operative_status"] == new_operative_status
    assert json_lib.loads(r5.data)["status"] == result


def assert_alerts(api_alert, db_alert):
    for key, value in api_alert.items():
        if key.startswith("_"):
            continue
        elif key == "the_geom":
            assert wkb_to_geojson(db_alert.the_geom) == value
            continue
        if isinstance(getattr(db_alert, key), datetime):
            assert getattr(db_alert, key).timestamp() == value
            continue
        assert getattr(db_alert, key) == value
