from unittest import TestCase

from nose.tools import assert_true, assert_equal

from tests.factories import NativeMetricFactory

from tests.helpers import not_raises


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
