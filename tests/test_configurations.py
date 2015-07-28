from unittest import TestCase

from mock import patch, PropertyMock
from nose.tools import assert_equal, assert_true, assert_in, raises

import kalibro_client
from kalibro_client.configurations.statistic import Statistic

from kalibro_client.configurations import MetricConfiguration, Reading, \
    KalibroRange
from kalibro_client.configurations.base import Base
from kalibro_client.miscellaneous import NativeMetric, CompoundMetric, Metric

from factories import KalibroConfigurationFactory, MetricConfigurationFactory, \
    ReadingGroupFactory, ReadingFactory, NativeMetricFactory,\
    CompoundMetricFactory, RangeSnapshotFactory, KalibroRangeFactory

from .helpers import not_raises

class TestConfigurationsBase(TestCase):
    @patch('kalibro_client.config')
    def test_service_address(self, kalibro_client_config):
        kalibro_client_config.return_value = kalibro_client.DEFAULT_CONFIG

        assert_equal(Base.service_address(), kalibro_client.DEFAULT_CONFIG['configurations_address'])
        kalibro_client_config.assert_called_once()

class TestKalibroConfiguration(TestCase):
    def setUp(self):
        self.subject = KalibroConfigurationFactory.build(id=1)
        self.metric_configuration = MetricConfigurationFactory.build()
        self.metric_configurations = [self.metric_configuration]

    def test_metric_configurations(self):
        metric_configurations_hash = {"metric_configurations": [self.metric_configuration._asdict()]}
        with patch.object(self.subject, 'request', return_value=metric_configurations_hash) as request_mock, \
             patch.object(MetricConfiguration, 'response_to_objects_array', return_value=self.metric_configurations) as mock:
            self.subject.metric_configurations()
            request_mock.assert_called_once_with(":id/metric_configurations", {'id': 1}, method='get')
            mock.assert_called_once_with(metric_configurations_hash)

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


class TestMetricConfiguration(TestCase):
    def setUp(self):
        self.subject = MetricConfigurationFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'reading_group_id'))
        assert_true(hasattr(self.subject, 'kalibro_configuration_id'))
        assert_true(hasattr(self.subject, 'weight'))
        assert_true(hasattr(self.subject, 'metric'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.kalibro_configuration_id = None
        self.subject.reading_group_id = None
        self.subject.weight = None

    def test_asdict(self):
        dict_ = self.subject._asdict()
        metric_dict = NativeMetricFactory.build()._asdict()
        assert_in('metric', dict_)
        assert_in(metric_dict, dict_.values())
        assert_equal(dict_['kalibro_configuration_id'], self.subject.kalibro_configuration_id)
        assert_equal(dict_['reading_group_id'], self.subject.reading_group_id)
        assert_equal(dict_['weight'], self.subject.weight)

    def test_metric_setter_with_native_metric(self):
        metric = NativeMetricFactory.build()
        self.subject.metric = metric._asdict()
        assert_true(isinstance(self.subject.metric, NativeMetric))
        assert_equal(self.subject.metric, metric)

    def test_metric_setter_with_compound_metric(self):
        metric = CompoundMetricFactory.build()
        self.subject.metric = metric._asdict()
        assert_true(isinstance(self.subject.metric, CompoundMetric))
        assert_equal(self.subject.metric, metric)

    def test_metric_setter_with_generic_metric(self):
        metric = CompoundMetricFactory.build()
        self.subject.metric = metric
        assert_true(isinstance(self.subject.metric, Metric))
        assert_equal(self.subject.metric, metric)

    @raises(ValueError)
    def test_metric_setter_with_something_that_isnt_a_metric(self):
        self.subject.metric = None

    def test_metric_configurations_of(self):
        response = {"metric_configurations": [self.subject._asdict()]}
        with patch.object(MetricConfiguration, 'request', return_value=response) as request_mock, \
            patch.object(MetricConfiguration, 'response_to_objects_array', return_value=[self.subject]) as response_to_array_mock:
            metric_configurations = MetricConfiguration.metric_configurations_of(self.subject.kalibro_configuration_id)
            request_mock.assert_called_once_with(
                '',
                {'id': self.subject.kalibro_configuration_id},
                method='get',
                prefix='kalibro_configurations/:id')
            response_to_array_mock.assert_called_once_with(response)
            assert_equal(metric_configurations, [self.subject])


class TestStatistic(object):
    def setUp(self):
        self.subject = Statistic()

    def test_metric_percentage(self):
        response = {"metric_percentage": 10.0}

        with patch.object(Statistic, 'request', return_value=response) as request_mock:
            result = Statistic.metric_percentage('test_metric')
            request_mock.assert_called_once_with('/metric_percentage',
                {'metric_code': 'test_metric'}, method='get')

            assert_equal(result, response)

    @raises(NotImplementedError)
    def test_not_implemented_find(self):
        Statistic.find(1)

    @raises(NotImplementedError)
    def test_not_implemented_all(self):
        Statistic.all()

    @raises(NotImplementedError)
    def test_not_implemented_exists(self):
        Statistic.exists(1)

    @raises(NotImplementedError)
    def test_not_implemented_save(self):
        self.subject.save()

    @raises(NotImplementedError)
    def test_not_implemented_update(self):
        self.subject.update()

    @raises(NotImplementedError)
    def test_not_implemented_delete(self):
        self.subject.delete()


class TestRangeSnapShot(TestCase):
    def setUp(self):
        self.subject = RangeSnapshotFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'beginning'))
        assert_true(hasattr(self.subject, 'end'))
        assert_true(hasattr(self.subject, 'grade'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.beginning = "-INF"
        self.subject.end = "INF"
        self.subject.grade = 5.6

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
