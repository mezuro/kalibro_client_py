from unittest import TestCase
from nose.tools import assert_equal, assert_true
from mock import patch

from kalibro_client.processor import Repository, TreeMetricResult

from tests.factories import TreeMetricResultFactory, DateMetricResultFactory, \
    KalibroModuleFactory, RepositoryFactory, NativeMetricFactory


class TestTreeMetricResult(TestCase):
    def setUp(self):
        self.subject = TreeMetricResultFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'aggregated_value'))

    def test_properties_setters(self):
        self.subject.aggregated_value = 3

    def test_aggregated_value_setter_with_none(self):
        self.subject.aggregated_value = None

        assert_equal(self.subject.aggregated_value, None)

    def test_aggregated_value_setter_with_string(self):
        self.subject.aggregated_value = "1.1"

        assert_equal(self.subject.aggregated_value, 1.1)

    def test_descendant_values(self):
        descendant_values_hash = {'descendant_values': ["1.1", "2.2", "3.3"]}
        descendant_values = [1.1, 2.2, 3.3]

        with patch.object(self.subject, 'request', return_value=descendant_values_hash) as request_mock:
            assert_equal(self.subject.descendant_values(), descendant_values)
            request_mock.assert_called_once_with(action=':id/descendant_values', params={'id': self.subject.id}, method='get')

    def test_history_of(self):
        date_metric_result = DateMetricResultFactory.build()
        kalibro_module = KalibroModuleFactory.build(id = 2)
        native_metric = NativeMetricFactory.build()
        repository = RepositoryFactory.build(id = 3)

        metric_result_history_of_hash = {'metric_result_history_of': [date_metric_result._asdict()]}
        with patch.object(Repository, 'request', return_value=metric_result_history_of_hash) as request_mock:
            assert_equal(TreeMetricResult.history_of(native_metric.name, kalibro_module.id,
                                                 repository.id),
                         [date_metric_result])
            request_mock.assert_called_once_with(action=':id/metric_result_history_of',
                                                 params={'metric_name': native_metric.name,
                                                         'kalibro_module_id': kalibro_module.id,
                                                         'id': repository.id})

    def test_asdict(self):
        dict = self.subject._asdict()

        assert_equal(self.subject.aggregated_value, dict["aggregated_value"])
