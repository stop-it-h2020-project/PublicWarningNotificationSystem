import json

import pytest

from translators import api_translators
from models.models import ResponsePlan
from .fixtures import ResponsePlanFactory2DB, ResponsePlanDictFactory


def assert_response_plans(response_plan_api, response_plan_db):
    # assert response_plan_db["id"] == response_plan_api[0]
    assert response_plan_db["response_plan_id"] == response_plan_api["response_plan_id"]
    assert response_plan_db["message_status"] == response_plan_api["message_status"]
    assert response_plan_db["alert_category"] == response_plan_api["alert_category"]
    assert response_plan_db["alert_severity"] == response_plan_api["alert_severity"]
    if isinstance(response_plan_db["actions"], list):
        assert response_plan_db["actions"] == response_plan_api["actions"]
    else:
        assert api_translators.actions_translator(
            response_plan_db["actions"]) == response_plan_api["actions"]
    if isinstance(response_plan_db["action_parameters"], list):
        assert response_plan_db["action_parameters"] == response_plan_api["action_parameters"]
    else:
        assert api_translators.action_parameters_translator(
            response_plan_db["action_parameters"]) == response_plan_api["action_parameters"]
    if isinstance(response_plan_db["action_format"], list):
        assert response_plan_db["action_format"] == response_plan_api["action_format"]
    else:
        assert api_translators.action_format_translator(
            response_plan_db["action_format"]) == response_plan_api["action_format"]
    if isinstance(response_plan_db["action_description"], list):
        assert response_plan_db["action_description"] == response_plan_api["action_description"]
    else:
        assert api_translators.action_description_translator(
            response_plan_db["action_description"]) == response_plan_api["action_description"]
    if isinstance(response_plan_db["action_body"], list):
        assert response_plan_db["action_body"] == response_plan_api["action_body"]
    else:
        assert api_translators.action_body_translator(
            response_plan_db["action_body"]) == response_plan_api["action_body"]
    if isinstance(response_plan_db["action_trigger"], list):
        assert response_plan_db["action_trigger"] == response_plan_api["action_trigger"]
    else:
        assert api_translators.action_trigger_translator(
            response_plan_db["action_trigger"]) == response_plan_api["action_trigger"]
    assert response_plan_db["accessibility"] == response_plan_api["accessibility"]
    assert response_plan_db["area"] == response_plan_api["area"]
    assert response_plan_db["geolocation"] == response_plan_api["geolocation"]


@pytest.mark.parametrize("test_input, test_input_2, test_output, test_output_2", [
    (["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_2", 20, 10, 40, "[10, 10]", "['email2@test.com', 'email3@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_2", 20, 10, 40, "[10, 10]", "['email2@test.com', 'email3@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"])
])
def test_get_response_plans_individual(api_client, orm_client,
                                       test_input, test_input_2, test_output, test_output_2):
    assert orm_client.session.query(ResponsePlan).count() == 0
    response_plan_1 = ResponsePlanFactory2DB(response_plan_id=test_input[0],
                                             message_status=test_input[1],
                                             alert_category=test_input[2],
                                             alert_severity=test_input[3],
                                             actions=test_input[4], action_parameters=test_input[5],
                                             action_format=test_input[6],
                                             action_description=test_input[7],
                                             action_body=test_input[8],
                                             action_trigger=test_input[9],
                                             accessibility=test_input[10], area=test_input[11],
                                             geolocation=test_input[12])
    assert orm_client.session.query(ResponsePlan).count() == 1
    response_plan_2 = ResponsePlanFactory2DB(response_plan_id=test_input_2[0],
                                             message_status=test_input_2[1],
                                             alert_category=test_input_2[2],
                                             alert_severity=test_input_2[3],
                                             actions=test_input_2[4],
                                             action_parameters=test_input_2[5],
                                             action_format=test_input_2[6],
                                             action_description=test_input_2[7],
                                             action_body=test_input_2[8],
                                             action_trigger=test_input_2[9],
                                             accessibility=test_input_2[10], area=test_input_2[11],
                                             geolocation=test_input_2[12])
    assert orm_client.session.query(ResponsePlan).count() == 2

    rv = api_client.get(f"/response-plans/{response_plan_1.internal_id}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_response_plans(response_content, response_plan_1.__dict__)

    rv = api_client.get(f"/response-plans/{response_plan_2.internal_id}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_response_plans(response_content, response_plan_2.__dict__)


@pytest.mark.parametrize("test_input, test_input_2, test_output, test_output_2", [
    (["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_2", 20, 10, 40, "[10, 10]", "['email2@test.com', 'email3@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_2", 20, 10, 40, "[10, 10]", "['email2@test.com', 'email3@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"])
])
def test_get_response_plans_all(api_client, orm_client,
                                test_input, test_input_2, test_output, test_output_2):
    assert orm_client.session.query(ResponsePlan).count() == 0
    response_plan_1 = ResponsePlanFactory2DB(response_plan_id=test_input[0],
                                             message_status=test_input[1],
                                             alert_category=test_input[2],
                                             alert_severity=test_input[3],
                                             actions=test_input[4], action_parameters=test_input[5],
                                             action_format=test_input[6],
                                             action_description=test_input[7],
                                             action_body=test_input[8],
                                             action_trigger=test_input[9],
                                             accessibility=test_input[10], area=test_input[11],
                                             geolocation=test_input[12])
    assert orm_client.session.query(ResponsePlan).count() == 1
    response_plan_2 = ResponsePlanFactory2DB(response_plan_id=test_input_2[0],
                                             message_status=test_input_2[1],
                                             alert_category=test_input_2[2],
                                             alert_severity=test_input_2[3],
                                             actions=test_input_2[4],
                                             action_parameters=test_input_2[5],
                                             action_format=test_input_2[6],
                                             action_description=test_input_2[7],
                                             action_body=test_input_2[8],
                                             action_trigger=test_input_2[9],
                                             accessibility=test_input_2[10], area=test_input_2[11],
                                             geolocation=test_input_2[12])
    assert orm_client.session.query(ResponsePlan).count() == 2

    rv = api_client.get(f"/response-plans/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_response_plans(response_content_1, response_plan_1.__dict__)
    assert_response_plans(response_content_2, response_plan_2.__dict__)


@pytest.mark.parametrize("test_input, test_output", [
    (["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"])
])
def test_get_response_plan(api_client, orm_client,
                           test_input, test_output):
    assert orm_client.session.query(ResponsePlan).count() == 0
    response_plan = ResponsePlanFactory2DB(response_plan_id=test_input[0],
                                           message_status=test_input[1],
                                           alert_category=test_input[2],
                                           alert_severity=test_input[3],
                                           actions=test_input[4], action_parameters=test_input[5],
                                           action_format=test_input[6],
                                           action_description=test_input[7],
                                           action_body=test_input[8],
                                           action_trigger=test_input[9],
                                           accessibility=test_input[10], area=test_input[11],
                                           geolocation=test_input[12])
    assert orm_client.session.query(ResponsePlan).count() == 1

    rv = api_client.get(f"/response-plans/{response_plan.internal_id}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_response_plans(response_content, response_plan.__dict__)


@pytest.mark.parametrize("test_input, test_output", [
    (["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"]),
    (["TEST_RESPONSE_PLAN_2", 20, 10, 40, "[10, 10]", "['email2@test.com', 'email3@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_2", 20, 10, 40, "[10, 10]", "['email2@test.com', 'email3@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"])
])
def test_add_response_plan(api_client, orm_client,
                           test_input, test_output):
    test_input[4] = json.loads(test_input[4])
    test_input[5] = json.loads(test_input[5].replace("'", "\""))
    test_input[6] = json.loads(test_input[6])
    test_input[7] = json.loads(test_input[7].replace("'", "\""))
    test_input[8] = json.loads(test_input[8].replace("'", "\""))
    test_input[9] = json.loads(test_input[9])

    assert orm_client.session.query(ResponsePlan).count() == 0
    response_plan = ResponsePlanDictFactory(response_plan_id=test_input[0],
                                            message_status=test_input[1],
                                            alert_category=test_input[2],
                                            alert_severity=test_input[3],
                                            actions=test_input[4], action_parameters=test_input[5],
                                            action_format=test_input[6],
                                            action_description=test_input[7],
                                            action_body=test_input[8],
                                            action_trigger=test_input[9],
                                            accessibility=test_input[10], area=test_input[11],
                                            geolocation=test_input[12])
    assert orm_client.session.query(ResponsePlan).count() == 0

    rv = api_client.post("/response-plans/", json=response_plan)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['internal_id']


@pytest.mark.parametrize("test_input, test_modify, test_output", [
    (["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email10@test.com', 'email20@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email10@test.com', 'email20@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"])
])
def test_update_response_plan(api_client, orm_client,
                              test_input, test_modify, test_output):
    test_modify[4] = json.loads(test_modify[4])
    test_modify[5] = json.loads(test_modify[5].replace("'", "\""))
    test_modify[6] = json.loads(test_modify[6])
    test_modify[7] = json.loads(test_modify[7].replace("'", "\""))
    test_modify[8] = json.loads(test_modify[8].replace("'", "\""))
    test_modify[9] = json.loads(test_modify[9])

    assert orm_client.session.query(ResponsePlan).count() == 0
    response_plan_orig = ResponsePlanFactory2DB(response_plan_id=test_input[0],
                                                message_status=test_input[1],
                                                alert_category=test_input[2],
                                                alert_severity=test_input[3],
                                                actions=test_input[4],
                                                action_parameters=test_input[5],
                                                action_format=test_input[6],
                                                action_description=test_input[7],
                                                action_body=test_input[8],
                                                action_trigger=test_input[9],
                                                accessibility=test_input[10], area=test_input[11],
                                                geolocation=test_input[12])
    assert orm_client.session.query(ResponsePlan).count() == 1

    response_plan_to_modify = ResponsePlanDictFactory(response_plan_id=test_modify[0],
                                                      message_status=test_modify[1],
                                                      alert_category=test_modify[2],
                                                      alert_severity=test_modify[3],
                                                      actions=test_modify[4],
                                                      action_parameters=test_modify[5],
                                                      action_format=test_modify[6],
                                                      action_description=test_modify[7],
                                                      action_body=test_modify[8],
                                                      action_trigger=test_modify[9],
                                                      accessibility=test_modify[10],
                                                      area=test_modify[11],
                                                      geolocation=test_modify[12])

    rv = api_client.put(f"/response-plans/{response_plan_orig.internal_id}",
                        json=response_plan_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(ResponsePlan).count() == 1

    rv = api_client.get(f"/response-plans/{response_plan_orig.internal_id}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_response_plans(response_content, response_plan_to_modify)


@pytest.mark.parametrize("test_input, test_delete", [
    (["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     [])
])
def test_delete_responseplan(api_client, orm_client,
                             test_input, test_delete):
    assert orm_client.session.query(ResponsePlan).count() == 0
    response_plan = ResponsePlanFactory2DB(response_plan_id=test_input[0],
                                           message_status=test_input[1],
                                           alert_category=test_input[2],
                                           alert_severity=test_input[3],
                                           actions=test_input[4],
                                           action_parameters=test_input[5],
                                           action_format=test_input[6],
                                           action_description=test_input[7],
                                           action_body=test_input[8],
                                           action_trigger=test_input[9],
                                           accessibility=test_input[10], area=test_input[11],
                                           geolocation=test_input[12])
    assert orm_client.session.query(ResponsePlan).count() == 1

    rv = api_client.delete(f"/response-plans/{response_plan.internal_id}")
    assert rv.status_code == 200

    assert orm_client.session.query(ResponsePlan).count() == 0


@pytest.mark.parametrize("test_input, test_input_2, test_output, test_output_2", [
    (["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_2", 20, 10, 40, "[10, 10]", "['email2@test.com', 'email3@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["TEST_RESPONSE_PLAN_2", 20, 10, 40, "[10, 10]", "['email2@test.com', 'email3@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"])
])
def test_get_response_plans_filtered_by_category(api_client, orm_client,
                                                 test_input, test_input_2, test_output,
                                                 test_output_2):
    assert orm_client.session.query(ResponsePlan).count() == 0
    response_plan_1 = ResponsePlanFactory2DB(response_plan_id=test_input[0],
                                             message_status=test_input[1],
                                             alert_category=test_input[2],
                                             alert_severity=test_input[3],
                                             actions=test_input[4],
                                             action_parameters=test_input[5],
                                             action_format=test_input[6],
                                             action_description=test_input[7],
                                             action_body=test_input[8],
                                             action_trigger=test_input[9],
                                             accessibility=test_input[10], area=test_input[11],
                                             geolocation=test_input[12])
    assert orm_client.session.query(ResponsePlan).count() == 1
    response_plan_2 = ResponsePlanFactory2DB(response_plan_id=test_input_2[0],
                                             message_status=test_input_2[1],
                                             alert_category=test_input_2[2],
                                             alert_severity=test_input_2[3],
                                             actions=test_input_2[4],
                                             action_parameters=test_input_2[5],
                                             action_format=test_input_2[6],
                                             action_description=test_input_2[7],
                                             action_body=test_input_2[8],
                                             action_trigger=test_input_2[9],
                                             accessibility=test_input_2[10], area=test_input_2[11],
                                             geolocation=test_input_2[12])
    assert orm_client.session.query(ResponsePlan).count() == 2

    rv = api_client.get(f"/response-plans/alert-category/10")
    assert rv.status_code == 200
    assert len(json.loads(rv.data)["data"]) == 2

    rv = api_client.get(f"/response-plans/alert-category/20")
    assert rv.status_code == 200
    assert len(json.loads(rv.data)["data"]) == 0
