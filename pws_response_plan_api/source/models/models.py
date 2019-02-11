from sqlalchemy import Column, String, Integer

from core.database import Base


# All the enums are defined in response_plan_validator.py
class ResponsePlan(Base):
    """
    Response plan table
    """
    __tablename__ = "response_plan"
    internal_id = Column(Integer, primary_key=True, nullable=False)
    response_plan_id = Column(String(128), unique=True, nullable=False)
    message_status = Column(Integer, nullable=False)  # Enum
    alert_category = Column(Integer, nullable=False)  # Enum
    alert_severity = Column(Integer)  # Enum
    actions = Column(String(256), nullable=False)  # Enum
    action_parameters = Column(String(256), nullable=False)
    action_format = Column(String(256), nullable=False)  # Enum
    action_description = Column(String(256), nullable=False)
    action_body = Column(String(256), nullable=False)
    action_trigger = Column(String(256), nullable=False)  # Enum
    accessibility = Column(Integer)  # Enum
    area = Column(String(256))
    geolocation = Column(String(256))

    def __str__(self):
        return (f"{self.internal_id}, {self.response_plan_id}, {self.message_status}, "
                f"{self.alert_category}, {self.alert_severity}, {self.actions}, "
                f"{self.action_parameters}, {self.action_format}, {self.action_description}, "
                f"{self.action_body}, {self.action_trigger}, {self.accessibility}, {self.area}, "
                f"{self.geolocation}")
