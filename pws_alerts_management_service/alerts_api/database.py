from sqlalchemy import create_engine, insert
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import g

from configmanager import ConfigManager

from .models import Base, Alert, Rule
from .auxiliary import construct_db_uri


def create_db_session(config=None):
    db_config = config or ConfigManager().get_specific_configuration("database")
    db_uri = construct_db_uri(db_config)
    engine = create_engine(db_uri)
    session = scoped_session(sessionmaker(bind=engine))
    return session


def get_db(api_app):
    if 'db' not in g:

        db = api_app.data.driver
        Base.metadata.bind = db.engine
        db.Model = Base
        g.db = db

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


class ORMClient:
    def __init__(self, database, user, host, password, port=5432):
        self.database = database
        self.user = user
        self.host = host
        self.port = port
        self.password = password
        self.engine = self.session = None
        self.connect()

    def connect(self):
        cmd = "postgresql://{}@{}:{}/{}".format(self.user, self.host, self.port, self.database)
        self.engine = create_engine(cmd)
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True,
                                                 bind=self.engine))
        self.session = db_session

    def create_tables(self):
        Base.metadata.create_all(self.engine, checkfirst=True)
        Alert.query = self.session.query_property()
        Rule.query = self.session.query_property()

    def clear_alerts(self):
        self.session.query(Alert).delete()
        self.session.commit()

    def insert_alert(self, data):
        self._insert(Alert, data)

    def insert_rule(self, data):
        self._insert(Rule, data)

    def _insert(self, model, data):
        self.session.execute(insert(model.__table__, values=data))
        self.session.commit()

    def close(self):
        self.session.close()
        self.engine.dispose()
        self.session = None
        self.engine = None
