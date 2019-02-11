import pytest

import validator


@pytest.mark.parametrize("test_input, test_output", [
    ("http://www.example.com", "True"),
    ("example.com", "False"),
    ([0], "False"),
    ([], "False"),
    ("", "False"),
    ("10, 20", "False"),
    (None, "False"),
])
def test_url_valid(test_input, test_output):
    assert eval(test_output) == validator.is_url_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    ("", "True"),
    ("10, 20", "True"),
    (10, "False"),
    ([10], "False"),
    ([], "False"),
    (None, "False"),
])
def test_message_valid(test_input, test_output):
    assert eval(test_output) == validator.is_message_valid(test_input)


@pytest.mark.parametrize("test_input, test_output", [
    (10, "True"),
    (20, "True"),
    (30, "True"),
    ([10], "False"),
    ([], "False"),
    ("", "False"),
    ("10, 20", "False"),
    (None, "False"),
])
def test_format_valid(test_input, test_output):
    assert eval(test_output) == validator.is_format_valid(test_input)
