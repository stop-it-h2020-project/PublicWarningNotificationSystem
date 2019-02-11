import pytest

from .fixtures import ResponsePlanFactory2DB


@pytest.mark.parametrize("test_input, test_output", [
    (["TEST_RESPONSE_PLAN_1", 20, 10, 40, "[10, 10]", "['email1@test.com', 'email2@test.com']",
      "[10, 10]", "['Sample description', '']", "['', '']", "[10, 10]", 10, "",
      "000000000140000000000000004010000000000000"],
     ["0, TEST_RESPONSE_PLAN_1, 20, 10, 40, [10, 10], ['email1@test.com', 'email2@test.com'], "
      "[10, 10], ['Sample description', ''], ['', ''], [10, 10], 10, "", "
      "000000000140000000000000004010000000000000"])
])
def test_responseplan_to_string(api_client, orm_client,
                                test_input, test_output):
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

    assert response_plan.__str__() == test_output[0]
