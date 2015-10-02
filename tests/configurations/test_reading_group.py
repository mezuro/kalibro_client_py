from unittest import TestCase

from mock import patch

from kalibro_client.configurations import Reading

from tests.factories import ReadingGroupFactory, ReadingFactory


class TestReadingGroup(TestCase):
    def setUp(self):
        self.subject = ReadingGroupFactory.build(id=1)
        self.reading = ReadingFactory.build()
        self.readings = [self.reading]

    def test_readings(self):
        readings_hash = {"readings": [self.reading._asdict()]}
        with patch.object(self.subject, 'request', return_value=readings_hash) as request_mock, \
             patch.object(Reading, 'response_to_objects_array', return_value=self.readings) as mock:
            self.subject.readings()
            request_mock.assert_called_once_with(":id/readings", {'id': 1}, method='get')
            mock.assert_called_once_with(readings_hash)


