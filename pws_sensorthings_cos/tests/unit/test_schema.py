import pytest

from mbconnector import mbcos

import subsystem
from configmanager import ConfigManager

schema_file_ds = "tests/unit/schema__ds.json"
schema_file_ms = "tests/unit/schema__ms.json"

conf_manager = ConfigManager()
mobility_config = conf_manager.get_specific_configuration("mobility").copy()
cos_config = conf_manager.get_specific_configuration("cos")
mobility_url = mobility_config.pop("url")


@pytest.mark.parametrize("data, sensor_id, schema_file",
    [
        ([1, 2, [3, 4]], "_ms_", schema_file_ms),
        ([1, 2, 3], "_ms_", schema_file_ds),
        ([1, 2, 3], "_ds_", schema_file_ms),
        (1, "_ms_", schema_file_ds),
        (1, "_ds_", schema_file_ms)
    ])
def test_unsupported_data(data, sensor_id, schema_file):

    cos_client = mbcos.CosObject(cos_config['object_type'], mobility_url, **mobility_config)
    cos_client.create_object()
    cos_client.set_schema_from_file(schema_file)

    ret = subsystem.generate_schema(data, cos_config, sensor_id)

    assert ret != schema_file


@pytest.mark.parametrize("data, sensor_id, schema_file",
    [
        ([1, 2, 3], "_ms_", schema_file_ms),
        (1, "_ds_", schema_file_ds)
    ])
def test_upported_data(data, sensor_id, schema_file):

    cos_client = mbcos.CosObject(cos_config['object_type'], mobility_url, **mobility_config)
    cos_client.create_object()
    cos_client.set_schema_from_file(schema_file)

    ret = subsystem.generate_schema(data, cos_config, sensor_id)

    assert ret != schema_file


@pytest.mark.parametrize("data, epoch, schema, cos_config, output",
    [
        (1, "2019-03-14T10:00:00.000Z", schema_file_ds, cos_config, {'date':
                                                                         {'value': '2019-03-14T10:00:00.000Z'},
                                                                     'value_0':
                                                                         {'value': 1,
                                                                          'time': '2019-03-14T10:00:00.000Z'},
                                                                     'sensorthing_id':
                                                                         {'value': 'sensorthings'}
                                                                     }),
        ([1, 2], "2019-03-14T10:00:00.000Z", schema_file_ms, cos_config, {'date':
                                                                              {'value': '2019-03-14T10:00:00.000Z'},
                                                                          'value_0':
                                                                              {'value': 1,
                                                                               'time': '2019-03-14T10:00:00.000Z'},
                                                                          'value_1':
                                                                              {'value': 2,
                                                                               'time': '2019-03-14T10:00:00.000Z'},
                                                                          'sensorthing_id':
                                                                              {'value': 'sensorthings'}
                                                                          })
    ])
def test_format_data(data, epoch, schema, cos_config, output):

    ret = subsystem.format_data(data, epoch, schema, cos_config)

    assert ret == output
