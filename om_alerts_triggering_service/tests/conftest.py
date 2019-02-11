import pytest
import os
import logging
from os.path import join, dirname, abspath

from .sql import *
from .fixtures import *
import configmanager
import configurelogging
import psycopg2
from postgresclient import db_utils, PostgresClient


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
    log_config = configmanager.ConfigManager().get_specific_configuration("logger")
    configurelogging.ConfigureLogging(**log_config)


@pytest.fixture(scope="session")
def db_conf():
    orig_config = configmanager.ConfigManager(test=True).get_specific_configuration("alerts_enricher")
    config = dict(
        host=orig_config["host"],
        port=orig_config["port"],
        user=orig_config["user"],
        password=orig_config["password"],
        database=orig_config["database"]
    )
    yield config


@pytest.fixture(scope="session", autouse=True)
def db_creation(db_conf):
    yield db_utils.create_db_with_extensions(**db_conf)
    db_utils.drop_db(**db_conf)


@pytest.fixture(scope="module")
def postgres_db(db_conf):
    orig_config = configmanager.ConfigManager(test=True).get_specific_configuration("alerts_enricher")
    connection = PostgresClient(**db_conf)
    yield connection
    connection.close()


@pytest.fixture(scope="function", autouse=True)
def clear_tables(postgres_db):
    postgres_db.execute_statement(TRUNCATE_TABLES, commit=True)
