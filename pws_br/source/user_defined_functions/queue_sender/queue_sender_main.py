from kapacitor.udf.agent import Agent
from queue_sender_service import QueueSenderHandler
from udf_handler import BaseHandler

if __name__ == '__main__':
    a = Agent()
    service = QueueSenderHandler()
    h = BaseHandler(a, service)
    a.handler = h

    a.start()
    a.wait()
