from typing import Union
import click
from sqlalchemy.exc import IntegrityError


from alerts_api.database import create_db_session
from alerts_api.models import Alert
from tests.fixtures import AlertFactory2DB, point_factory


db_session = create_db_session()
AlertFactory2DB._meta.sqlalchemy_session = db_session


@click.command("new_alert")
@click.argument('id_')
@click.argument('latitude')
@click.argument('longitude')
def new_alert(id_: int, latitude: Union[int, float], longitude: Union[int, float]):
    """Creates an alert with dummy values in the given coordinates."""
    try:
        AlertFactory2DB(id=id_, the_geom=point_factory(float(latitude), float(longitude)))
        click.echo(f"Adding alert '{id_}'' at lat: {latitude}, long: {longitude}")
    except IntegrityError as exc_info:
        print(exc_info.args[0])
        db_session.rollback()
        exit(-1)

    count = db_session.query(Alert).count()
    click.echo(f"Now, there are {count} alerts in the database.")


@click.command("clear_alerts")
def clear_alerts():
    """Delete all Alerts from database."""
    returned = db_session.query(Alert).delete()
    db_session.commit()

    db_uri = db_session.get_bind().__repr__()
    click.echo(f"Deleted {returned} alerts from database {db_uri}.")
