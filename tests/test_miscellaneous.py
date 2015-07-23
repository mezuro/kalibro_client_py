from unittest import TestCase

from nose.tools import assert_true

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


class TestCompoudMetric(TestCase):
    def setUp(self):
        self.subject = CompoundMetricFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'script'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.script = "test"