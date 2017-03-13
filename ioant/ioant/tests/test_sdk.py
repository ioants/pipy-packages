import unittest
import mock

from ioant.sdk import IOAnt
from ioant import utils


class SDKTestCase(unittest.TestCase):
    """Tests for `sdk.py`."""

    def setUp(self):
        self.ioant = IOAnt(None, None)

    def test_get_topic_from_string(self):
        """get topic from string"""
        valid_test_topic = 'live/kil/runneval/tempy/0/1'
        result = self.ioant.get_topic_from_string(valid_test_topic)
        self.assertEqual(result['top'], 'live')
        self.assertEqual(result['global'], 'kil')
        self.assertEqual(result['local'], 'runneval')
        self.assertEqual(result['client_id'], 'tempy')
        self.assertEqual(result['message_type'], 0)
        self.assertEqual(result['stream_index'], 1)

    def test_get_topic_from_string_invalid(self):
        """get topic from string"""
        invalid_test_topic = 'live/kil/asd/runneval/tempy/0/1'
        result = self.ioant.get_topic_from_string(invalid_test_topic)
        self.assertIsNone(result)

    def test_get_empty_topic_structure(self):
        """get empty topic structure"""
        result = self.ioant.get_topic_structure()
        self.assertEqual(result['top'], '+')
        self.assertEqual(result['global'], '+')
        self.assertEqual(result['local'], '+')
        self.assertEqual(result['client_id'], '+')
        self.assertEqual(result['message_type'], -1)
        self.assertEqual(result['stream_index'], -1)

    @mock.patch("ioant.sdk.mqtt.Client")
    @mock.patch("ioant.sdk.IOAnt.mqtt_client")
    def test_setup(self, mocked_ioant_mqtt, mocked_mqtt_client):
        """Create a default Trigger message"""
        test_configuration = '{ \
            "ioant" : { \
                "mqtt" : { \
                    "global" : "global", \
                    "local" : "local", \
                    "client_id" : "boilerplate", \
                    "broker" : "ioant.com", \
                    "user" : "hero", \
                    "password" : "test", \
                    "port" : 1883 \
                 }, \
                "communication_delay" : 5000, \
                "latitude" : 0.0, \
                "longitude" : 0.0, \
                "app_generic_a" : 0, \
                "app_generic_b" : 0, \
                "app_generic_c" : 0 \
            } \
        }'
        mocked_mqtt_client.return_value = mocked_ioant_mqtt
        config_dict = utils.json_string_to_dict(test_configuration)
        self.ioant.setup(config_dict)

        # Assert that Paho MQTT client was initiated with correct client_id
        mocked_mqtt_client.assert_called_with(config_dict['ioant']['mqtt']['client_id'])

        # Assert that connect attempt to broker was done with configuration parameters
        mocked_ioant_mqtt.connect.assert_called_with(config_dict['ioant']['mqtt']['broker'],
                                                     config_dict['ioant']['mqtt']['port'],
                                                     60)

        # Assert that connect attempt to broker was done with configuration parameters
        mocked_ioant_mqtt.connect.assert_called_with(config_dict['ioant']['mqtt']['broker'],
                                                     config_dict['ioant']['mqtt']['port'],
                                                     60)

        # Assert that device topic is set as expected
        expected_topic = self.ioant.get_topic_structure()
        expected_topic['top'] = 'live'
        expected_topic['global'] = config_dict['ioant']['mqtt']['global']
        expected_topic['local'] = config_dict['ioant']['mqtt']['local']
        expected_topic['client_id'] = config_dict['ioant']['mqtt']['client_id']

        self.assertEqual(self.ioant.device_topic, expected_topic)
