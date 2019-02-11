#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from configurelogging import ConfigureLogging
from configmanager import ConfigManager
from postgresclient import db_utils

from api import create_app
from core.database import session
from resources.resources_loader import Resources

config = ConfigManager().configuration
ConfigureLogging(**config["logger"])

db_utils.create_db_with_extensions(**config["database"])

app, _ = create_app()

if __name__ == '__main__':
    Resources.init_cors(app)
    app.run(host="0.0.0.0", debug=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
