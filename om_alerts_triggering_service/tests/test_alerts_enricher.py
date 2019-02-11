import pytest
import requests
import json
from .fixtures import *
from oms_alerts_processor_service.enricher import AlertEnricher
from .sql import *


def test_enriched_tiltmeter_alert(monkeypatch):

    def fake_cos_get(cos_api_url):
        class FakeResponse(object):
            def __init__(self):
                self.status_code = 200
                self.content = json.dumps(TILTMETER_COS_RESPONSE)

        return FakeResponse()

    monkeypatch.setattr(requests, 'get', fake_cos_get)

    alerts_enricher = AlertEnricher()
    rule, alert = alerts_enricher.validate_and_traslate(TILTEMETER_ALERT)
    assert alert == ENRICHED_TILTMETER_ALERT


def test_fail_enriched_tiltmeter_alert(monkeypatch):
    def fake_cos_get(cos_api_url):
        class FakeResponse(object):
            def __init__(self):
               self.status_code = 404

            def raise_for_status(self):
               raise requests.exceptions.HTTPError

        return FakeResponse()

    monkeypatch.setattr(requests, 'get', fake_cos_get)

    alerts_enricher = AlertEnricher()
    rule, alert = alerts_enricher.validate_and_traslate(TILTEMETER_ALERT)

    assert alert["the_geom"]["coordinates"] is None

# TODO Improve this test. It doesn't work.
# @pytest.mark.parametrize("wrong_alert_in",
#                          [TILTEMETER_ALERT_NO_RELATED_ITEM,
#                           TILTEMETER_ALERT_NO_ITEM_TYPE,
#                           TILTEMETER_ALERT_UNSUPPORTED_TYPE
#                           ])
# def test_ko_format(wrong_alert_in):
#
#     with pytest.raises(ValueError) as e_info:
#         alerts_enricher = AlertEnricher()
#         alerts_enricher.validate_and_traslate(wrong_alert_in)
