from unittest import TestCase

from mock import patch
from nose.tools import assert_equal, assert_true

from kalibro_client.configurations import Reading

from tests.factories import ReadingFactory

from tests.helpers import not_raises


class TestReading(TestCase):
    def setUp(self):
        self.subject = ReadingFactory.build()
        self.readings = [self.subject]

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'reading_group_id'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.reading_group_id = None

    def test_readings_of(self):
        readings_hash = {"readings": [self.subject._asdict()]}
        reading_group_id = 1
        with patch.object(Reading, 'request', return_value=readings_hash) as request_mock, \
             patch.object(Reading, 'response_to_objects_array', return_value=self.readings) as mock:
            Reading.readings_of(reading_group_id)
            request_mock.assert_called_once_with(action='', params={}, method='get', prefix="reading_groups/{}".format(reading_group_id))
            mock.assert_called_once_with(readings_hash)

    def test_save_prefix(self):
        assert_equal(self.subject.save_prefix(), "reading_groups/{}".format(self.subject.reading_group_id))

    def test_update_prefix(self):
        assert_equal(self.subject.update_prefix(), "reading_groups/{}".format(self.subject.reading_group_id))

    def test_delete_prefix(self):
        assert_equal(self.subject.delete_prefix(), "reading_groups/{}".format(self.subject.reading_group_id))



