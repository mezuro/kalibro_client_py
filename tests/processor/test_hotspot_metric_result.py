from unittest import TestCase
from nose.tools import assert_equal, assert_true, raises
from mock import patch

from tests.factories import HotspotMetricResultFactory

from tests.helpers import not_raises


class TestHotspotMetricResult(TestCase):
    def setUp(self):
        self.subject = HotspotMetricResultFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'line_number'))
        assert_true(hasattr(self.subject, 'message'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.line_number = 1
        self.subject.message = "test message"

    @raises(ValueError)
    def test_properties_setters_with_invalid_parameters(self):
        self.subject.line_number = "string"

    def test_asdict(self):
        dict_ = self.subject._asdict()

        assert_equal(None, dict_["value"])
        assert_equal(self.subject.metric_configuration_id, dict_["metric_configuration_id"])
        assert_equal(self.subject.line_number, dict_["line_number"])
        assert_equal(self.subject.message, dict_["message"])

    def test_related_results(self):
        related_results = [HotspotMetricResultFactory.build(id=id_) for id_ in range(3)]
        related_results_hash = {'hotspot_metric_results': [related_result._asdict()
                                                           for related_result in related_results]}

        with patch.object(self.subject, 'request', return_value=related_results_hash) as request_mock:
            assert_equal(self.subject.related_results(), related_results)
            request_mock.assert_called_once_with(action=':id/related_results', params={'id': self.subject.id},
                                                 method='get')
