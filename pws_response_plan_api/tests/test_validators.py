import pytest

from validators import api_validator


@pytest.mark.parametrize("test_input, test_output", [
    ("ID_1", "True"),
    ("", "False"),
    (None, "False"),
])
def test_response_plan_id_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_response_plan_id_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    (10, "True"),
    (20, "True"),
    (0, "False"),
    ("ID_1", "False"),
    ("", "False"),
    (None, "False"),
])
def test_message_status_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_message_status_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    (10, "True"),
    (20, "True"),
    (30, "True"),
    (40, "True"),
    (50, "True"),
    (60, "True"),
    (70, "True"),
    (80, "True"),
    (90, "True"),
    (100, "True"),
    (110, "True"),
    (200, "True"),
    (300, "True"),
    (0, "False"),
    ("GEO", "False"),
    ("MET", "False"),
    ("", "False"),
    (None, "False"),
])
def test_alert_category_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_alert_category_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    (10, "True"),
    (20, "True"),
    (30, "True"),
    (40, "True"),
    (50, "True"),
    (100, "True"),
    (0, "False"),
    ("", "False"),
    (None, "False"),
])
def test_alert_severity_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_alert_severity_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    ([10], "True"),
    ([20], "True"),
    ([30], "True"),
    ([10, 20, 30], "True"),
    ([0, 10], "False"),
    ("", "False"),
    ("10, 20", "False"),
    (None, "False"),
])
def test_actions_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_actions_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    (['hola@hola.com'], "True"),
    ("", "False"),
    ("10, 20", "False"),
    (None, "False"),
])
def test_action_parameters_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_action_parameters_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    ([10], "True"),
    ([20], "True"),
    ([30], "True"),
    ([10, 20, 30], "True"),
    ([0, 10], "False"),
    ("", "False"),
    ("10, 20", "False"),
    (None, "False"),
])
def test_action_format_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_action_formats_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    (["Sample description..."], "True"),
    (["Sample description...", "descrip 2"], "True"),
    ("Sample description...", "False"),
    ("", "False"),
    (None, "False"),
])
def test_action_description_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_action_descriptions_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    (["Sample body..."], "True"),
    (["Sample body...", "body 2"], "True"),
    ("Sample body...", "False"),
    ("", "False"),
    (None, "False"),
])
def test_action_body_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_action_bodys_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    ([10], "True"),
    ([20], "True"),
    ([10, 20], "True"),
    ("0", "False"),
    ("Automatic", "False"),
    ("Manual", "False"),
    ("True", "False"),
    ("False", "False"),
    ("", "False"),
    (None, "False"),
])
def test_action_trigger_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_action_triggers_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    (10, "True"),
    (20, "True"),
    (0, "False"),
    ("Administrator", "False"),
    ("Operator", "False"),
    ("", "False"),
    (None, "False"),
])
def test_accessibility_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_accessibility_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    ("Sample area description...", "True"),
    ("", "True"),
    (None, "False"),
])
def test_area_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_area_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    ("000000000140000000000000004010000000000000", "True"),
    ("00000000140000000000000004010000000000000", "False"),
    ("POINT()", "False"),
    ("", "False"),
    (None, "False"),
])
def test_geolocation_valid(test_input, test_output):
    assert eval(test_output) == api_validator.is_geolocation_valid(test_input)
