from functools import partial
import factory

from models.models import ResponsePlan
from translators import api_translators


def dict_factory(factory, **kwargs):
    return factory.stub(**kwargs).__dict__


# TODO Improve as
# https://bitbucket.org/worldsensing_traffic/om_task_management_service/src/develop/task_management_api/factories.py
class AbstractResponsePlanFactory(factory.Factory):
    class Meta:
        model = ResponsePlan
        abstract = True

    internal_id = factory.Sequence(lambda n: int(n))
    response_plan_id = "TEST_RESPONSE_PLAN_1"
    message_status = 20
    alert_category = 10
    alert_severity = 40
    actions = [10, 10]
    action_parameters = ["email1@test.com", "email2@test.com"]
    action_format = [10, 10]
    action_description = ["Sample description", ""]
    action_body = ["This is an email to send...", ""]
    action_trigger = [10, 10]
    accessibility = 10
    area = ""
    geolocation = "000000000140000000000000004010000000000000"


class ResponsePlanFactory(AbstractResponsePlanFactory):
    pass


ResponsePlanFactory._meta.exclude = ("internal_id",)

ResponsePlanDictFactory = partial(dict_factory, ResponsePlanFactory)


class ResponsePlanFactory2DB(AbstractResponsePlanFactory, factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        # sqlalchemy_session = create_db_session
        sqlalchemy_session_persistence = "commit"
