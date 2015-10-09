from unittest import TestCase
from nose.tools import assert_equal, assert_true, raises
from mock import patch, Mock

from kalibro_client.processor import MetricCollectorDetails
from kalibro_client.errors import KalibroClientNotFoundError, KalibroClientRequestError

from tests.factories import MetricCollectorDetailsFactory, NativeMetricFactory

from tests.helpers import not_raises


class TestMetricCollectorDetails(TestCase):
    def setUp(self):
        self.subject = MetricCollectorDetailsFactory.build()
        self.native_metric = NativeMetricFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'supported_metrics'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.supported_metrics = None

    def test_supported_metrics_conversion_from_hash(self):
        supported_metrics_hash = {self.native_metric.code: self.native_metric._asdict()}

        self.subject.supported_metrics = supported_metrics_hash

        assert_equal(self.subject.supported_metrics, {self.native_metric.code: self.native_metric})

    def test_find_metric_by_name(self):
        name = self.native_metric.name

        assert_equal(self.subject.find_metric_by_name(name), self.native_metric)

    def test_asdict(self):
        dict = self.subject._asdict()

        assert_equal(self.subject.name, dict["name"])
        assert_equal(self.subject.description, dict["description"])
        assert_equal(self.subject.supported_metrics, dict["supported_metrics"])

    def test_find_by_name(self):
        with patch.object(MetricCollectorDetails, 'request',
                          return_value={'metric_collector_details': self.subject._asdict()}) as metric_collector_details_request:
            assert_equal(MetricCollectorDetails.find_by_name(self.subject.name), self.subject)

            metric_collector_details_request.assert_called_once_with('find', params={"name": self.subject.name})

    @raises(KalibroClientNotFoundError)
    def test_find_by_name_invalid_collector(self):
        error_response = {'error': "Metric Collector '{}' not found.".format(self.subject.name)}
        response = Mock()
        response.json = Mock(return_value=error_response)
        with patch.object(MetricCollectorDetails, 'request') as metric_collector_details_request:
            metric_collector_details_request.side_effect=KalibroClientRequestError(response)
            MetricCollectorDetails.find_by_name(self.subject.name)
            metric_collector_details_request.assert_called_once

    def test_all_names(self):
        names = ['Analizo', 'MetricFu']
        with patch.object(MetricCollectorDetails, 'request',
                          return_value={'metric_collector_names': names}) as metric_collector_details_request:
            all_names = MetricCollectorDetails.all_names()
            assert_equal(all_names, names)
            metric_collector_details_request.assert_called_once_with('names', method='get')

    def test_all(self):
        with patch.object(MetricCollectorDetails, 'request',
                          return_value=[self.subject._asdict()]) as metric_collector_details_request:
            all_metric_collectors = MetricCollectorDetails.all()
            assert_equal(all_metric_collectors, [self.subject])
            metric_collector_details_request.assert_called_once_with('', method='get')
