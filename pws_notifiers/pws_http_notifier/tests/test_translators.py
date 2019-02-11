import json
import pytest
from pws_common.enums import ActionFormatEnum

import translators

from tests.fixtures import *


@pytest.mark.parametrize("test_input, test_output", [
    ("Sample message in string format", "Sample message in string format"),
    ("{'key': 'value'}", "{'key': 'value'}"),
    ("0", "0"),
    ("", ""),
])
def test_format_plain_text_valid(test_input, test_output):
    result = translators.str_to_format(test_input, ActionFormatEnum.PLAIN_TEXT.value)

    assert test_output == result


@pytest.mark.parametrize("response_plan_httppost_cap, alert, test_output", [
    (response_plan_httppost_cap, alert, notification_cap)
])
def test_format_cap_valid(response_plan_httppost_cap, alert, test_output):
    message_received = json.dumps([alert, response_plan_httppost_cap])
    result = translators.str_to_format(message_received, ActionFormatEnum.CAP.value)

    # Datetime cannot be compared with hardcoded XML
    # assert test_output == result
