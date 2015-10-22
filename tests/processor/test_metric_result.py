from unittest import TestCase
from nose.tools import assert_equal, assert_true
from mock import patch

from kalibro_client.configurations import MetricConfiguration
from kalibro_client.processor import MetricResult

from tests.factories import MetricResultFactory, MetricConfigurationFactory, \
    ModuleResultFactory

from tests.helpers import not_raises


class TestMetricResult(TestCase):
    def setUp(self):
        self.subject = MetricResultFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'value'))
        assert_true(hasattr(self.subject, 'metric_configuration_id'))
        assert_true(hasattr(self.subject, 'module_result_id'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.value = 3
        self.subject.metric_configuration_id = 4
        self.subject.module_result_id = 4

    def test_value_setter_with_none(self):
        self.subject.value = None

        assert_equal(self.subject.value, None)

    def test_value_setter_with_string(self):
        self.subject.value = "1.1"

        assert_equal(self.subject.value, 1.1)

    def test_metric_configuration_id_setter_with_none(self):
        self.subject.metric_configuration_id = None

        assert_equal(self.subject.metric_configuration_id, None)

    def test_metric_configuration_id_setter_with_string(self):
        self.subject.metric_configuration_id = "42"

        assert_equal(self.subject.metric_configuration_id, 42)

    def test_asdict(self):
        dict = self.subject._asdict()

        assert_equal(self.subject.value, dict["value"])
        assert_equal(self.subject.metric_configuration_id, dict["metric_configuration_id"])

    def test_metric_configuration(self):
        metric_configuration = MetricConfigurationFactory.build()
        with patch.object(MetricConfiguration, 'find', return_value=metric_configuration) as find_mock:
            assert_equal(self.subject.metric_configuration(), metric_configuration)
            find_mock.assert_called_once_with(self.subject.metric_configuration_id)

    def test_module_result_when_module_result_is_none(self):
        module_result = ModuleResultFactory.build()
        response = {'module_result': module_result._asdict()}
        with patch.object(MetricResult, 'request',
                          return_value=response) as request_mock:
            assert_equal(self.subject.module_result(), module_result)
            request_mock.assert_called_once_with(action=':id/module_result',
                                                 params={'id': self.subject.id},
                                                 method='get')

    def test_module_result_when_module_result_is_not_none(self):
        module_result = ModuleResultFactory.build(id=1)
        self.subject._module_result = module_result
        assert_equal(self.subject.module_result(), module_result)
