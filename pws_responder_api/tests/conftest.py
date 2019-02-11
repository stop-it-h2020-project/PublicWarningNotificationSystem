import os
import logging
from os.path import join, dirname, abspath

import pytest
import configmanager
from configurelogging import ConfigureLogging
from configmanager import ConfigManager

from api import create_app


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


@pytest.fixture(scope="module", autouse=True)
def api_client():
    app = create_app()
    yield app.test_client()

@pytest.fixture(scope="session", autouse=True)
def set_environment(request):
    current = os.environ.get("PROJECT_ROOT", None)
    route = abspath(join(dirname(__file__), "."))
    os.environ["PROJECT_ROOT"] = route
    yield
    # teardown
    if current:
        os.environ["PROJECT_ROOT"] = current


@pytest.fixture(scope="session", autouse=True)
def configure_logging(set_environment):
    log_config = configmanager.ConfigManager(test=True).get_specific_configuration("logger")
    ConfigureLogging(**log_config)

