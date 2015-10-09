from unittest import TestCase

from mock import patch, PropertyMock

from nose.tools import assert_equal, assert_true

from kalibro_client.configurations import Reading, KalibroRange

from tests.factories import ReadingFactory, KalibroRangeFactory
from tests.helpers import not_raises


class TestKalibroRange(TestCase):
    def setUp(self):
        self.subject = KalibroRangeFactory.build()
        self.reading = ReadingFactory.build()
        self.kalibro_ranges = [self.subject]

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'beginning'))
        assert_true(hasattr(self.subject, 'end'))
        assert_true(hasattr(self.subject, 'reading_id'))
        assert_true(hasattr(self.subject, 'metric_configuration_id'))
        assert_true(hasattr(self.subject, 'comments'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.beginning = 0.0
        self.subject.end = 10.0
        self.subject.reading_id = 1
        self.subject.metric_configuration_id = 2
        self.subject.comments = None

    def test_reading(self):
        with patch.object(Reading, 'find', return_value=self.reading) as reading_find:
            assert_equal(self.subject.reading, self.reading)
            reading_find.assert_called_once_with(self.subject.reading_id)

    def patch_reading(self):
        return patch.object(type(self.subject), 'reading', new_callable=PropertyMock, return_value=self.reading)

    def test_label(self):
        with self.patch_reading() as reading_mock:
            assert_equal(self.subject.label, self.reading.label)
            reading_mock.assert_called_once()

    def test_grade(self):
        with self.patch_reading() as reading_mock:
            assert_equal(self.subject.grade, self.reading.grade)
            reading_mock.assert_called_once()

    def test_color(self):
        with self.patch_reading() as reading_mock:
            assert_equal(self.subject.color, self.reading.color)
            reading_mock.assert_called_once()

    def test_ranges_of(self):
        kalibro_ranges_hash = {"kalibro_ranges": [self.subject._asdict()]}

        with patch.object(KalibroRange, 'request', return_value=kalibro_ranges_hash) as request_mock, \
             patch.object(KalibroRange, 'response_to_objects_array', return_value=self.kalibro_ranges) as kalibro_ranges_mock:

            assert_equal(KalibroRange.ranges_of(self.subject.id), self.kalibro_ranges)
            request_mock.assert_called_once_with('', params={"id": self.subject.id}, method='get', prefix="metric_configurations/:id")
            kalibro_ranges_mock.assert_called_once_with(kalibro_ranges_hash)

    def test_asdict(self):
        dict_ = self.subject._asdict()

        assert_equal(dict_['reading_id'], self.subject.reading_id)
        assert_equal(dict_['metric_configuration_id'], self.subject.metric_configuration_id)

    def test_save_prefix(self):
        assert_equal(self.subject.save_prefix(), "metric_configurations/{}".format(self.subject.metric_configuration_id))

    def test_update_prefix(self):
        assert_equal(self.subject.update_prefix(), "metric_configurations/{}".format(self.subject.metric_configuration_id))

    def test_delete_prefix(self):
        assert_equal(self.subject.delete_prefix(), "metric_configurations/{}".format(self.subject.metric_configuration_id))
