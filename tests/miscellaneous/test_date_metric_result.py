from unittest import TestCase
import dateutil.parser

from nose.tools import assert_true, assert_equal, assert_is_not_none, \
    raises

from tests.factories import DateMetricResultFactory, MetricResultFactory


class TestDateMetricResult(TestCase):
    def setUp(self):
        self.metric_result = MetricResultFactory.build()
        self.subject = DateMetricResultFactory.build()
        self.second_subject = DateMetricResultFactory.build(date=None, metric_result = self.metric_result)

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'date'))
        assert_true(hasattr(self.subject, 'metric_result'))

    @raises(AttributeError)
    def test_properties_setter_date(self):
        self.subject.date = None

    @raises(AttributeError)
    def test_properties_setter_metric_result(self):
        self.subject.metric_result = None

    def test_constructor(self):
        assert_equal(self.subject.date, dateutil.parser.parse(DateMetricResultFactory.date))
        assert_equal(self.second_subject.date, None)
        assert_equal(self.second_subject.metric_result, self.metric_result)

        assert_is_not_none(self.subject.metric_result)
        metric_result = self.subject.metric_result
        metric_result_params = DateMetricResultFactory.metric_result

        assert_equal(metric_result.value, float(metric_result_params["value"]))
        assert_equal(metric_result.module_result_id,
                     metric_result_params["module_result_id"])
        assert_equal(metric_result.metric_configuration_id,
                     metric_result_params["metric_configuration_id"])

    def test_asdict(self):
        dict = self.subject._asdict()

        assert_equal(self.subject.metric_result._asdict(), dict["metric_result"])

        return dict
