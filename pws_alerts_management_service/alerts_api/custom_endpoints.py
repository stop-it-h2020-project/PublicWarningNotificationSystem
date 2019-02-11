from flask import current_app, jsonify
from .database import get_db


def distinct_field_in_alerts(field):
    db = get_db(current_app)
    distinct_query = f"select DISTINCT {field} from alerts;"
    ret = db.engine.execute(distinct_query)
    result = [x[0] for x in ret]
    return jsonify(_items=result)


def add_custom_endpoints(app):
    app.add_url_rule("/alerts/distinct/<field>", "distinct_field", distinct_field_in_alerts)
