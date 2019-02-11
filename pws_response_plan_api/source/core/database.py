from configmanager import ConfigManager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from utils import construct_db_uri

db_config = ConfigManager().get_specific_configuration("database")
db_uri = construct_db_uri(db_config)
engine = create_engine(db_uri, convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=True,
                                      bind=engine))

Base = declarative_base()
Base.query = session.query_property()
metadata = Base.metadata


def init_db():
    import models.models
    Base.metadata.create_all(engine, checkfirst=True)


def insert_response_plan(response_plan):
    from models.models import ResponsePlan
    session.add(response_plan)
    session.flush()
    internal_id = response_plan.internal_id
    session.commit()

    return internal_id


def get_response_plans(alert_category):
    from models.models import ResponsePlan
    if alert_category:
        return session.query(ResponsePlan).filter_by(alert_category=alert_category)
    else:
        return session.query(ResponsePlan)


def get_response_plan(response_plan_id):
    from models.models import ResponsePlan
    return session.query(ResponsePlan).filter_by(internal_id=response_plan_id).first()


def get_response_plan_external_id(response_external_id):
    from models.models import ResponsePlan
    return session.query(ResponsePlan).filter_by(response_plan_id=response_external_id).first()


def update_response_plan(response_plan_id, response_plan):
    from models.models import ResponsePlan
    session.query(ResponsePlan) \
        .filter_by(internal_id=response_plan_id) \
        .update(response_plan)
    session.commit()

    return response_plan_id


def delete_response_plan(response_plan_id):
    from models.models import ResponsePlan
    session.query(ResponsePlan) \
        .filter_by(internal_id=response_plan_id) \
        .delete()
    session.commit()

    return response_plan_id


def clear_response_plans():
    from models.models import ResponsePlan
    session.query(ResponsePlan).delete()
    session.commit()


def close():
    session.close()
    engine.dispose()
