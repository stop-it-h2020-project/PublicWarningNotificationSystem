import json

from kapacitor.udf import udf_pb2
from kapacitor.udf.agent import Handler
import udf_types


class BaseHandler(Handler):
    def __init__(self, agent, service):
        self._agent = agent
        self.service = service
        self.types = {}
        self.types[udf_types.BOOL] = udf_pb2.BOOL
        self.types[udf_types.INT] = udf_pb2.INT
        self.types[udf_types.DOUBLE] = udf_pb2.DOUBLE
        self.types[udf_types.STRING] = udf_pb2.STRING
        self.types[udf_types.DURATION] = udf_pb2.DURATION

    def info(self):
        response = udf_pb2.Response()
        response.info.wants = udf_pb2.BATCH
        response.info.provides = udf_pb2.STREAM
        options = self.service.get_options()
        for option in options:
            response.info.options[option].valueTypes.append(
                self.types[options[option]])

        return response

    def init(self, init_req):
        response = udf_pb2.Response()
        try:
            self.service.init(init_req.options)
            response.init.success = True
        except Exception as e:
            response.init.error = str(e)
        return response

    def snapshot(self):
        response = udf_pb2.Response()
        response.snapshot.snapshot = json.dumps(
            self.service.snapshot())
        return response

    def restore(self, restore_req):
        response = udf_pb2.Response()
        try:
            data = json.loads(restore_req.snapshot)
            self.service.restore(data)
            response.restore.success = True
        except Exception as e:
            response.restore.error = str(e)
        return response

    def begin_batch(self, begin_req):
        self.service.begin_batch(begin_req)
        # raise Exception("not supported")

    def point(self, point):
        response = udf_pb2.Response()
        response.point.CopyFrom(point)
        response.point.ClearField('fieldsInt')
        response.point.ClearField('fieldsString')
        response.point.ClearField('fieldsDouble')

        self.service.process_point(point)

    def end_batch(self, end_req):
        self.service.end_batch(end_req)
        # raise Exception("not supported")
