from unittest import TestCase
from kalibro_client.configurations.base import Base
from kalibro_client.configurations import MetricConfiguration, Reading

import kalibro_client

from nose.tools import assert_equal

from mock import patch
from factories import KalibroConfigurationFactory, MetricConfigurationFactory, \
    ReadingGroupFactory, ReadingFactory

class TestConfigurationsBase(TestCase):
    @patch('kalibro_client.config')
    def test_service_address(self, kalibro_client_config):
        kalibro_client_config.return_value = kalibro_client.DEFAULT_CONFIG

        assert_equal(Base.service_address(), kalibro_client.DEFAULT_CONFIG['configurations_address'])
        kalibro_client_config.assert_called_once()

class TestKalibroConfiguration(TestCase):
    def setUp(self):
        self.subject = KalibroConfigurationFactory.build()
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

    def test_metric_configurations(self):
        readings_hash = {"readings": [self.reading._asdict()]}
        with patch.object(self.subject, 'request', return_value=readings_hash) as request_mock, \
             patch.object(Reading, 'response_to_objects_array', return_value=self.readings) as mock:
            self.subject.readings()
            request_mock.assert_called_once_with(":id/readings", {'id': 1}, method='get')
            mock.assert_called_once_with(readings_hash)
