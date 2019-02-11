import pytest
import datetime
import pytz

import subsystem


timestamp = datetime.datetime.strftime(datetime.datetime.utcnow().replace(tzinfo=pytz.utc), "%Y-%m-%dT%H:%M:%SZ")

@pytest.mark.parametrize("in_data",
    [{'nodeModel': 'LS-G6-INC15',
                          'commMetaData':
                              {'networkId': '13797',
                               'macAddress': 76553340,
                               'receivedTimestamp': '2018-09-21T08:43:50Z',
                               'frequencyHertz': 868.85,
                               'snr': 11,
                               'sequenceCounter': [1],
                               'gatewayId': 12273815315514654977,
                               'rssi': -73,
                               'type': 'longRangeRadioMetaDataV1',
                               'sf': 9,
                               'macType': 'ETSIV1'
                               },
                          'nodeId': 10,
                          'readings':
                              [{'temperature': 27.02930684452094,
                                'axisTwo': 2085694
                                }
                               ],
                          'readTimestamp': '2018-09-21T08:43:49Z',
                          'type': 'tiltReadingsV1'
                          }])
def test_wrong_schema(in_data):
    ret = subsystem.get_data(in_data, timestamp)   # in_data is missing Tiltmeter's axisTwo
    assert ret is None


@pytest.mark.parametrize("in_data",
    [{'nodeModel': 'LS-G6-INC15',
                          'commMetaData':
                              {'networkId': '13797',
                               'macAddress': 76553340,
                               'receivedTimestamp': '2018-09-21T08:43:50Z',
                               'frequencyHertz': 868.85,
                               'snr': 11,
                               'sequenceCounter': [1],
                               'gatewayId': 12273815315514654977,
                               'rssi': -73,
                               'type': 'longRangeRadioMetaDataV1',
                               'sf': 9,
                               'macType': 'ETSIV1'
                               },
                          'nodeId': 10,
                          'readings':
                              [{'axisTwo': 979382,
                                'temperature': 27.02930684452094,
                                'axisOne': 2085694
                                }
                               ],
                          'readTimestamp': '2018-09-21T08:43:49Z',
                          'type': 'tiltReadingsV1'
      }
     ]
)
def test_correct_schema(in_data):
    ret = subsystem.get_data(in_data, timestamp)
    assert ret is not None