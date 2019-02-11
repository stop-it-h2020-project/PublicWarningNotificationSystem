from sqlalchemy import Column, Integer, Float, String, ForeignKey, event
from sqlalchemy.orm import validates, relationship

from .common import (CommonColumns, _validate_the_geom, utc_now,
                     RULE_ID_TYPE, GEO_TYPE, DT_TYPE)


ALERT_RESOLVED_STATUS = 30  # TODO get from configuration


class Rule(CommonColumns):
    __tablename__ = "rules"

    id = Column(RULE_ID_TYPE, primary_key=True)
    name = Column(String(64))
    # Measurement
    measure_name = Column(String(64))  # speed, load, inclination
    measure_unit = Column(String(64))  # km/s, cars/m2 ...
    reference_type = Column(String(64))  # out of range, threshold, in range
    reference_start = Column(Float)  # 30 kmh
    reference_end = Column(Float, nullable=True)  # 50 kmh, nullable if unidimensional reference

    # Model and algorithm data
    algorithm = Column(String(64))  # roughly the algorithm used
    algorithm_description = Column(String(265))  # purpose and design
    algorithm_comment = Column(String(256))  # for changes
    algorithm_owner = Column(String(256))  # the name of the creator or a link to the wikipedia
    based_on_rule = Column(String(64))  # a rule_id from which this one is based
    time_window_duration_s = Column(Float)  # if the algorithm is time-bound


class Alert(CommonColumns):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rule = relationship(Rule)
    rule_id = Column(RULE_ID_TYPE, ForeignKey('rules.id'))

    title = Column(String(256))
    description = Column("description", String(256))
    recurrence = Column(Integer, default=1)  # Whether it was raised once or more

    resolved_at = Column(DT_TYPE, default=None)
    # Operator IDs
    assigned_to = Column(String(64))  # currently handling
    created_by = Column(String(64))
    updated_by = Column(String(64))
    resolved_by = Column(String(64))

    # Item information retrieved from another object or subsystem
    related_item_id = Column(String(32))
    related_item_type = Column(String(32))
    address = Column(String(256))  # Human location, km. point, street, building

    the_geom = Column(GEO_TYPE)

    # Alert typing
    meta_type = Column(String(32))
    type = Column(Integer)
    sub_type = Column(String(32))

    absolute_value = Column(Float)
    absolute_difference = Column(Float)  # From expected / forecasted value
    score_value = Column(Float)
    # Percentage is computed downstream

    # Alert multi-status. Naming will be decide downstream
    severity = Column(Integer)  # Given by the BRE
    status = Column(Integer, default=0)  # General status regarding creation and resolution
    operative_status = Column(Integer, default=0)  # Given by the operators handling

    @validates("the_geom")
    def validate_the_geom(self, _, geom):
        return _validate_the_geom(geom)


@event.listens_for(Alert.operative_status, 'set')
def alert_resolved_set(target, new_status, old_status, initiator):
    """Set resolved_at timestamp whe operative status changes to resolved"""
    if new_status == ALERT_RESOLVED_STATUS and old_status < ALERT_RESOLVED_STATUS:
        target.resolved_at = utc_now()

