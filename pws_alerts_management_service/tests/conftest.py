import pytest
import os
import logging
from os.path import join, dirname, abspath

from configmanager import ConfigManagerTest
from postgresclient import db_utils

from alerts_api import api, database
from .fixtures import AlertFactory2DB, RuleFactory2DB


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


@pytest.fixture(scope="session")
def db_conf():
    yield ConfigManagerTest().get_specific_configuration("database")


@pytest.fixture(scope="session", autouse=True)
def db_creation(db_conf):
    yield db_utils.create_db_with_extensions(**db_conf)
    db_utils.drop_db(**db_conf)


@pytest.fixture(scope="module", autouse=True)
def api_client(db_conf):
    api.EVE_SETTINGS["SQLALCHEMY_DATABASE_URI"] = api.construct_db_uri(db_conf)
    api.EVE_SETTINGS["TESTING"] = True
    api.EVE_SETTINGS["DEBUG"] = True
    api.EVE_SETTINGS["ALERT_STREAM"] = False
    app, db = api.create_app(settings=api.EVE_SETTINGS)
    AlertFactory2DB._meta.sqlalchemy_session = db.session
    RuleFactory2DB._meta.sqlalchemy_session = db.session
    # TODO Flask way of DB ORM client
    # with app.app_context():
    #     app.init_db()
    yield app.test_client()
    db.session.close()
    db.engine.dispose()


@pytest.fixture(scope="function")
def clear_tables(db_conf):
    yield
    session = database.create_db_session(db_conf)
    for name, table in database.Base.metadata.tables.items():
        session.execute(table.delete())
    session.commit()
    session.close()


@pytest.fixture(scope="function")
def orm_client(db_conf):
    client = database.ORMClient(**db_conf)
    client.create_tables()
    yield client
    client.clear_alerts()
    client.close()
