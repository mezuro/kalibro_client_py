from unittest import TestCase

from mock import patch
from nose.tools import assert_equal, assert_true, assert_in, raises

from kalibro_client.configurations import MetricConfiguration
from kalibro_client.miscellaneous import NativeMetric, CompoundMetric, Metric,\
    HotspotMetric

from tests.factories import MetricConfigurationFactory, NativeMetricFactory, \
    CompoundMetricFactory, HotspotMetricFactory

from tests.helpers import not_raises

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

    def test_metric_setter_with_hotspot_metric(self):
        metric = HotspotMetricFactory.build()
        self.subject.metric = metric._asdict()
        assert_true(isinstance(self.subject.metric, HotspotMetric))
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


