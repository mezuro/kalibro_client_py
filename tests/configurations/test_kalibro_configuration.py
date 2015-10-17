from unittest import TestCase
from mock import patch

from kalibro_client.configurations import MetricConfiguration
from tests.factories import KalibroConfigurationFactory, MetricConfigurationFactory


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

    def test_hotspot_metric_configurations(self):
        hotspot_metric_configurations_hash = {"hotspot_metric_configurations": [self.metric_configuration._asdict()]}
        with patch.object(self.subject, 'request', return_value=hotspot_metric_configurations_hash) as request_mock, \
             patch.object(MetricConfiguration, 'response_to_objects_array', return_value=self.metric_configurations) as mock:
            self.subject.hotspot_metric_configurations()
            request_mock.assert_called_once_with(":id/hotspot_metric_configurations", {'id': 1}, method='get')
            mock.assert_called_once_with({'metric_configurations': hotspot_metric_configurations_hash['hotspot_metric_configurations']})

    def test_tree_metric_configurations(self):
        tree_metric_configurations_hash = {"tree_metric_configurations": [self.metric_configuration._asdict()]}
        with patch.object(self.subject, 'request', return_value=tree_metric_configurations_hash) as request_mock, \
             patch.object(MetricConfiguration, 'response_to_objects_array', return_value=self.metric_configurations) as mock:
            self.subject.tree_metric_configurations()
            request_mock.assert_called_once_with(":id/tree_metric_configurations", {'id': 1}, method='get')
            mock.assert_called_once_with({'metric_configurations': tree_metric_configurations_hash['tree_metric_configurations']})
