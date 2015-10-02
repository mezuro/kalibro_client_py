from unittest import TestCase

from nose.tools import assert_true

from tests.factories import RangeSnapshotFactory

from tests.helpers import not_raises


class TestRangeSnapShot(TestCase):
    def setUp(self):
        self.subject = RangeSnapshotFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'beginning'))
        assert_true(hasattr(self.subject, 'end'))
        assert_true(hasattr(self.subject, 'grade'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.beginning = "-INF"
        self.subject.end = "INF"
        self.subject.grade = 5.6
