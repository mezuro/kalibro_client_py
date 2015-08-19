from unittest import TestCase, skip
from datetime import datetime
import dateutil.parser

from nose.tools import assert_true, assert_equal, assert_is_not_none, \
    assert_almost_equal, raises

from mock import Mock

from factories import NativeMetricFactory, CompoundMetricFactory, \
    DateMetricResultFactory, DateModuleResultFactory, MetricResultFactory, \
    ModuleResultFactory
from .helpers import not_raises

from kalibro_client.miscellaneous import Granularity, DateMetricResult


class TestNativeMetric(TestCase):
    def setUp(self):
        self.subject = NativeMetricFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'languages'))
        assert_true(hasattr(self.subject, 'metric_collector_name'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.metric_collector_name = "test"
        self.subject.languages = ["test"]

    def test_asdict(self):
        dict_ = self.subject._asdict()
        assert_equal(dict_['languages'], self.subject.languages)
        assert_equal(dict_['metric_collector_name'],
                     self.subject.metric_collector_name)


class TestCompoudMetric(TestCase):
    def setUp(self):
        self.subject = CompoundMetricFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'script'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.script = "test"

    @raises(ValueError)
    def test_properties_setters(self):
        self.subject.script = None

    def test_asdict(self):
        dict_ = self.subject._asdict()
        assert_equal(dict_['script'], self.subject.script)


# This does not subclass TestCase so test generators work
class TestGranularity(object):
    # Note: since we've delegated the implementation of the comparisons to the
    # enum module they won't be tested here

    def test_parent(self):
        def check_parent(child, parent):
            assert_equal(child.parent(), parent)

        # This runs runs the check_parent method with the given parameters as a
        # test. It differs from simply calling assert in that each is an
        # individual test and can fail or succeed on it's own,
        yield check_parent, Granularity.METHOD, Granularity.CLASS
        yield check_parent, Granularity.CLASS, Granularity.PACKAGE
        yield check_parent, Granularity.PACKAGE, Granularity.SOFTWARE
        yield check_parent, Granularity.SOFTWARE, Granularity.SOFTWARE

    def test_str(self):
        assert_equal(str(Granularity.SOFTWARE), 'SOFTWARE')

    def test_comparisons(self):
        def check_equality(granularity1, granularity2):
            assert_true(granularity1 == granularity2)

        yield check_equality, Granularity.SOFTWARE, Granularity.SOFTWARE
        yield check_equality, Granularity.PACKAGE, Granularity.PACKAGE
        yield check_equality, Granularity.CLASS, Granularity.CLASS
        yield check_equality, Granularity.METHOD, Granularity.METHOD
        yield check_equality, Granularity.FUNCTION, Granularity.FUNCTION

        def check_greater_than(granularity1, granularity2):
            assert_true(granularity1 > granularity2)

        yield check_greater_than, Granularity.SOFTWARE, Granularity.PACKAGE
        yield check_greater_than, Granularity.PACKAGE, Granularity.CLASS
        yield check_greater_than, Granularity.CLASS, Granularity.METHOD

        def check_lesser_than(granularity1, granularity2):
            assert_true(granularity1 < granularity2)

        yield check_lesser_than, Granularity.PACKAGE, Granularity.SOFTWARE
        yield check_lesser_than, Granularity.CLASS, Granularity.PACKAGE
        yield check_lesser_than, Granularity.METHOD, Granularity.CLASS
        yield check_lesser_than, Granularity.FUNCTION, Granularity.PACKAGE

    @raises(ValueError)
    def test_invalid_lt_comparisons(self):
        Granularity.METHOD < Granularity.FUNCTION

    @raises(ValueError)
    def test_invalid_eq_comparisons(self):
        Granularity.CLASS == Granularity.FUNCTION

    @raises(ValueError)
    def test_invalid_gt_comparisons(self):
        Granularity.CLASS > Granularity.FUNCTION


class TestDateModuleResult(object):
    def setUp(self):
        self.subject = DateModuleResultFactory.build()
        self.module_result = ModuleResultFactory.build()
        self.second_subject = DateModuleResultFactory.build(date=None, module_result = self.module_result)

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'date'))
        assert_true(hasattr(self.subject, 'module_result'))

    @raises(AttributeError)
    def test_properties_setters(self):
        self.subject.date = "2011-10-20T18:27:43.151+00:00"
        self.subject.module_result = self.module_result

    def test_result(self):
        assert_equal(self.subject.result(), self.module_result.grade)

    def test_constructor(self):
        assert_equal(self.subject.date, dateutil.parser.parse(DateModuleResultFactory.date))
        assert_equal(self.second_subject.date, None)
        assert_equal(self.second_subject.module_result, self.module_result)

        assert_is_not_none(self.subject.module_result)
        module_result = self.subject.module_result
        module_result_params = DateModuleResultFactory.module_result

        assert_equal(module_result.grade, float(module_result_params["grade"]))
        assert_equal(module_result.parent_id, module_result_params["parent_id"])
        assert_equal(module_result.processing_id, module_result_params["processing_id"])

    def test_asdict(self):
        dict = self.subject._asdict()

        assert_equal(self.subject.module_result._asdict(), dict["module_result"])

        return dict


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
