from unittest import TestCase

from nose.tools import assert_true, assert_equal, raises

from tests.factories import CompoundMetricFactory
from tests.helpers import not_raises


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
