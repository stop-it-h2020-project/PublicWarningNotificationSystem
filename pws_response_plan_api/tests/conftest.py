import os
import logging
from os.path import join, dirname, abspath

import pytest
import configurelogging
from configmanager import ConfigManagerTest
from postgresclient import db_utils

from api import create_app
from .fixtures import ResponsePlanFactory2DB
from core import database
from utils import construct_db_uri

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def set_environment():
    current = os.environ.get("PROJECT_ROOT", None)
    route = abspath(join(dirname(__file__), "."))
    os.environ["PROJECT_ROOT"] = route
    yield
    # teardown
    if current:
        os.environ["PROJECT_ROOT"] = current


@pytest.fixture(scope="session", autouse=True)
def configure_logging(set_environment):
    log_config = ConfigManagerTest().get_specific_configuration("logger")
    configurelogging.ConfigureLogging(**log_config)


@pytest.fixture(scope="session")
def db_conf():
    yield ConfigManagerTest().get_specific_configuration("database")


@pytest.fixture(scope="session", autouse=True)
def db_creation(db_conf):
    db_utils.create_db_with_extensions(**db_conf)
    yield
    db_utils.drop_db(**db_conf)


@pytest.fixture(scope="module", autouse=True)
def api_client(db_conf):
    SQLALCHEMY_SETTINGS = {
        "DEBUG": True,
        "SQLALCHEMY_DATABASE_URI": construct_db_uri(db_conf),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

    app, db = create_app(settings=SQLALCHEMY_SETTINGS)
    ResponsePlanFactory2DB._meta.sqlalchemy_session = db.session
    yield app.test_client()
    db.session.close()
    db.engine.dispose()


@pytest.fixture(scope="function")
def clear_tables(db_conf):
    yield
    session = database.session
    for name, table in database.metadata.tables.items():
        session.execute(table.delete())
    session.commit()
    session.close()


@pytest.fixture(scope="function")
def orm_client(db_conf):
    client = database
    client.init_db()
    yield client
    ResponsePlanFactory2DB.reset_sequence(value=0, force=True)
    client.clear_response_plans()
    client.close()
