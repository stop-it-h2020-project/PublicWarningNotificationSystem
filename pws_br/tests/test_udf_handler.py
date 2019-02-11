import unittest
import json
import mock
from kapacitor.udf import udf_pb2
from source.user_defined_functions import udf_types, udf_handler


class TestUdfHandler(unittest.TestCase):
    def setUp(self):
        self.agent = mock.Mock()
        self.service = mock.Mock()
        self.handler = udf_handler.BaseHandler(self.agent, self.service)

    def test_creation(self):
        # Check that agent and service are stored
        self.assertEqual(self.agent, self.handler._agent)
        self.assertEqual(self.service, self.handler.service)

    def test_init(self):
        self.service.init.return_value = None
        options = {}
        init_req = mock.Mock()
        init_req.options = options
        response = self.handler.init(init_req)
        self.assertTrue(response.init.success)
        self.service.init.assert_called_with(options)

    def test_init_failure(self):
        msg = "All wrong!"
        self.service.init.side_effect = Exception(msg)
        options = {}
        init_req = mock.Mock()
        init_req.options = options
        response = self.handler.init(init_req)
        self.assertFalse(response.init.success)
        self.assertEqual(msg, response.init.error)
        self.service.init.assert_called_with(options)

    def test_info(self):
        options = {
            "option1": udf_types.STRING,
            "option2": udf_types.INT,
            "option3": udf_types.BOOL,
            "option4": udf_types.DURATION,
            "option5": udf_types.DOUBLE
        }
        self.service.get_options.return_value = options
        response = self.handler.info()
        self.assertEqual(response.info.options["option1"].valueTypes[0],
                         udf_pb2.STRING)
        self.assertEqual(response.info.options["option2"].valueTypes[0],
                         udf_pb2.INT)
        self.assertEqual(response.info.options["option3"].valueTypes[0],
                         udf_pb2.BOOL)
        self.assertEqual(response.info.options["option4"].valueTypes[0],
                         udf_pb2.DURATION)
        self.assertEqual(response.info.options["option5"].valueTypes[0],
                         udf_pb2.DOUBLE)

    def test_snapshot(self):
        snapshot = {"data": [0, 1, 2]}
        self.service.snapshot.return_value = snapshot
        response = self.handler.snapshot()
        self.assertEqual(json.dumps(snapshot), response.snapshot.snapshot)

    def test_restore(self):
        snapshot = '{"data": "this is a snapshot"}'
        restore_req = mock.Mock()
        restore_req.snapshot = snapshot
        response = self.handler.restore(restore_req)
        self.assertTrue(response.restore.success)

    def test_restore_wrong_json(self):
        snapshot = '{"data": "this is a snapshot"'
        restore_req = mock.Mock()
        restore_req.snapshot = snapshot
        response = self.handler.restore(restore_req)
        self.assertFalse(response.restore.success)

    def test_restore_error(self):
        snapshot = '{"data": "this is a snapshot"}'
        msg = "All wrong!"
        self.service.restore.side_effect = Exception(msg)
        restore_req = mock.Mock()
        restore_req.snapshot = snapshot
        response = self.handler.restore(restore_req)
        self.assertFalse(response.restore.success)
        self.assertEqual(msg, response.restore.error)

    # Ignore test, we dont have any point processing yet
    @mock.patch("kapacitor.udf.udf_pb2.Response")
    def test_point(self, mock_response):
        point = mock.Mock()
        values = {
            "values": {
                "val1": 12.3,
                "val2": 15.6
            },
            "tags": {
                "sensor_id": "1"
            }
        }
        # self.service.process_point.return_value = values
        # self.agent.write_response = mock.Mock()
        # self.handler.point(point)
        # self.service.process_point.assert_called_once_with(point)
        # self.assertTrue(self.agent.write_response.called)
        # response = self.agent.write_response.call_args
        # response.point.tags.update.assert_called_once_with(values["tags"])
