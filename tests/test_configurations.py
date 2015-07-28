from unittest import TestCase
from kalibro_client.configurations.base import Base
from kalibro_client.configurations import MetricConfiguration, Reading

from kalibro_client.miscellaneous import NativeMetric, CompoundMetric, Metric

import kalibro_client

from nose.tools import assert_equal, assert_true, assert_in, raises

from mock import patch
from factories import KalibroConfigurationFactory, MetricConfigurationFactory, \
    ReadingGroupFactory, ReadingFactory, NativeMetricFactory,\
    CompoundMetricFactory

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
