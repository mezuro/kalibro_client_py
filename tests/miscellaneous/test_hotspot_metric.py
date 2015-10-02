from unittest import TestCase

from nose.tools import assert_equal

from tests.factories import HotspotMetricFactory


class TestHotspotMetric(TestCase):
    def setUp(self):
        self.subject = HotspotMetricFactory.build()

    def test_type(self):
        assert_equal('HotspotMetricSnapshot', self.subject.type)

    def test_scope(self):
        assert_equal('SOFTWARE', self.subject.scope)
