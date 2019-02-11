from functools import partial
import factory
from alerts_api.models import Alert, Rule


class RuleFactory2DB(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Rule
        sqlalchemy_session_persistence = "commit"

    name = "High speed, medium penalty"
    measure_name = "spped"
    measure_unit = "kph"
    reference_type = "superior threshold"
    reference_start = 50.1
    reference_end = 100
    algorithm = "New algorithm"
    algorithm_owner = "Bruce Wayne"
    time_window_duration_s = 10.001


class AbstractAlertFactory(factory.Factory):
    class Meta:
        model = Alert
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    meta_type = "data"
    type = 10
    sub_type = "N/A"
    status = 0
    operative_status = 0
    severity = 70
    title = factory.LazyAttributeSequence(
        lambda o, n: "Inclination threshold exceeded for tiltmeter [%s]" % (n + 1021))
    description = "Axis one of tiltmeter exceeded [1] degree threshold during more than 2 minutes"


class AlertFactory(AbstractAlertFactory):
    pass


AlertFactory._meta.exclude = ("id",)


class AlertFactory2DB(AbstractAlertFactory, factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        # sqlalchemy_session = create_db_session
        sqlalchemy_session_persistence = "commit"


AlertDictFactory = partial(factory.build, dict, FACTORY_CLASS=AlertFactory)


def point_factory(latitude, longitude):
    return {"coordinates": [longitude, latitude], "type": "Point"}


automatic_response = {
    "data": [
        {
            "internal_id": 1,
            "response_plan_id": "TEST_RESPONSE_PLAN_5",
            "message_status": 20,
            "alert_category": 10,
            "alert_severity": 10,
            "actions": [
                30
            ],
            "action_parameters": [
                "http://test.com"
            ],
            "action_format": [
                10
            ],
            "action_description": "Sample description for HTTP",
            "action_trigger": [10],
            "action_body": ["cuerpesito"],
            "action_severity": [40],
            "accessibility": 10,
            "area": "",
            "geolocation": "000000000140000000000000004010000000000000"
        }
    ]
}

manual_response = {
    "data": [
        {
            "internal_id": 1,
            "response_plan_id": "TEST_RESPONSE_PLAN_5",
            "message_status": 20,
            "alert_category": 10,
            "alert_severity": 10,
            "actions": [
                30
            ],
            "action_parameters": [
                "http://test.com"
            ],
            "action_format": [
                10
            ],
            "action_description": "Sample description for HTTP",
            "action_trigger": [20],
            "action_body": ["cuerpesito"],
            "action_severity": [40],
            "accessibility": 10,
            "area": "",
            "geolocation": "000000000140000000000000004010000000000000"
        }
    ]
}