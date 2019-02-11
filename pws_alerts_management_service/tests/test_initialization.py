import pytest

from postgresclient import PostgresClient

from alerts_api.database import ORMClient
from alerts_api.models import Base


#TODO move outside db_creation
@pytest.mark.second
def test_create_table(db_conf):
    orm_client = ORMClient(**db_conf)
    Base.metadata.create_all(orm_client.engine)
    client = PostgresClient(**db_conf)
    statement = """SELECT EXISTS (SELECT 1 FROM information_schema.tables
            WHERE table_catalog = '{}' AND table_name = 'alerts') AS exists;""".format(
        db_conf["database"]
    )
    result = client.execute_statement(statement, close=True, fetch=True)[0]["exists"]
    assert result == True
    client.close()
    orm_client.close()
