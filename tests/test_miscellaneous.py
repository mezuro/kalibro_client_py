from unittest import TestCase

from nose.tools import assert_true, assert_equal, raises

from factories import NativeMetricFactory, CompoundMetricFactory

from .helpers import not_raises

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
        assert_equal(dict_['languages'], ["RUBY"])
        assert_equal(dict_['metric_collector_name'], "MetricFu")


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
        assert_equal(dict_['script'], "return 0;")