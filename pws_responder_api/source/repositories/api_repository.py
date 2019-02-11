import json
from enum import IntEnum

from utils import queue_sender


class Action(IntEnum):
    EMAIL = 10
    SMS = 20
    HTTP_POST = 30

    def __str__(self):
        return str(self.value)


class ApiRepository:
    def __init__(self, rabbit_config):
        self.message_publisher = queue_sender.QueueSender(rabbit_config)

    def execute_response(self, data):
        response_plan = data["response_plan"]
        alert = json.dumps(data["alert"])
        actions = response_plan["actions"]
        parameters = response_plan["action_parameters"]
        formats = response_plan["action_format"]
        bodies = response_plan["action_body"]

        for idx, action in enumerate(actions):
            parameter = parameters[idx]
            body = bodies[idx]
            format = formats[idx]
            if action == Action.EMAIL:
                self.send_email(parameter, body, alert)
            elif action == Action.SMS:
                self.send_sms(parameter, body, alert)
            elif action == Action.HTTP_POST:
                self.send_httppost(parameter, body, format, alert)
            else:
                raise AttributeError("Action [" + str(action) + "] not supported. Supported actions: "
                                     "[10 (Email), 20 (SMS), 30 (HTTP POST)]")

    def send_email(self, parameter, body, alert):
        self.message_publisher.publish({"message_html": body,
                                        "receiver_emails": parameter,
                                        "title": "PWS Notification",
                                        "queue": "pws.notifications.email"
                                        })

    def send_sms(self, parameter, body, alert):
        self.message_publisher.publish({"message": body,
                                        "receiver_phones": parameter,
                                        "queue": "pws.notifications.sms"
                                        })

    def send_httppost(self, parameter, body, format, alert):
        self.message_publisher.publish({"message": body,
                                        "url": parameter,
                                        "format": format,
                                        "queue": "pws.notifications.http"
                                        })
