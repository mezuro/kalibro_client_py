from unittest import TestCase

from nose.tools import assert_true, assert_equal, raises

from factories import NativeMetricFactory, CompoundMetricFactory
from .helpers import not_raises

from kalibro_client.miscellaneous import Granularity


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
