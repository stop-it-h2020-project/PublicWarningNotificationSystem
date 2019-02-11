#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from configurelogging import ConfigureLogging
from configmanager import ConfigManager
from postgresclient import db_utils

from alerts_api.api import create_app


config = ConfigManager().configuration
ConfigureLogging(**config["logger"])
db_utils.create_db_with_extensions(**config["database"])
app, db = create_app()

# NOTE Use "flask run"
# if __name__:
#    app.run(host="0.0.0.0", debug=False, use_reloader=False)
