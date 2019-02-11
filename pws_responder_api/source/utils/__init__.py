# -*- coding: utf-8 -*-
"""
Utils methods.
"""
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            # For consistency with the API, we add the timezone marker Z
            return o.isoformat() + "Z"
        else:
            return json.JSONEncoder.default(self, o)


class JSONDecoder:
    def __init__(self):
        pass

    def decode(self, text):
        return json.loads(text)
