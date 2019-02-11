import pytest

from .fixtures import *


@pytest.mark.parametrize("response_plan, alert, result",
    [
        (response_plan_email, alert, 200),
        (response_plan_email_no_email, alert, 500),
        (response_plan_sms, alert, 200),
        (response_plan_sms_no_phone, alert, 500),
        (response_plan_httppost, alert, 200),
        (response_plan_httppost_no_url, alert, 500),
        (response_plan_unkown_action, alert, 500)
    ]
)
def test_notify(api_client, response_plan, alert, result):
    data = {"data": {"response_plan": response_plan, "alert": alert}}
    response = api_client.post("/responder", json=data)
    assert response.status_code == result

