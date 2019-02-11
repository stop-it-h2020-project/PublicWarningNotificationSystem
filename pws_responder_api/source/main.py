# -*- coding: utf-8 -*-
import logging

from configurelogging import ConfigureLogging
from configmanager import ConfigManager

from resources.resources_loader import Resources
from api import create_app

app = create_app()

logger = logging.getLogger(__name__)


def init_config(config=None):
    """
    Initialize the server with the endpoints.
    Args:
        config:
    """
    if config is None:
        config = ConfigManager().configuration
    else:
        config = config
    ConfigureLogging(**config["logger"])
    app.config.update(**config)


app = create_app()
init_config()

# Only enter when run in local
if __name__ == '__main__':
    Resources.init_cors(app)
    app.run(debug=True, host='0.0.0.0')
