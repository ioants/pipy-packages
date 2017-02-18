import unittest
from ioant.ioant import ioant as ioant_core


class IoantTestCase(unittest.TestCase):
    """Tests for `utils.py`."""

    def test_get_topic_from_string(self):
        """get topic from string"""
        ioant = ioant_core.Ioant(None)
        valid_test_topic = 'live/kil/runneval/tempy/0/1'
        result = ioant.get_topic_from_string(valid_test_topic)
        self.assertEqual(result['global'], 'kil')
        self.assertEqual(result['local'], 'runneval')
        self.assertEqual(result['client_id'], 'tempy')
        self.assertEqual(result['message_type'], 0)
        self.assertEqual(result['stream_index'], 1)

    def test_get_topic_from_string_invalid(self):
        """get topic from string"""
        ioant = ioant_core.Ioant(None)
        invalid_test_topic = 'live/kil/asd/runneval/tempy/0/1'
        result = ioant.get_topic_from_string(invalid_test_topic)
        self.assertIsNone(result)

    def test_get_empty_topic(self):
        """get empty topic structure"""
        ioant = ioant_core.Ioant(None)
        result = ioant.get_topic()
        self.assertEqual(result['top'], '+')
        self.assertEqual(result['global'], '+')
        self.assertEqual(result['local'], '+')
        self.assertEqual(result['client_id'], '+')
        self.assertEqual(result['message_type'], -1)
        self.assertEqual(result['stream_index'], -1)

    def test_create_message(self):
        """get empty topic structure"""
        ioant = ioant_core.Ioant(None)
        result_message = ioant.create_message("Trigger")
        self.assertEqual(result_message.extra, 0)
