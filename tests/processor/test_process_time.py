from unittest import TestCase
from nose.tools import assert_equal, assert_true

from tests.factories import ProcessTimeFactory

from tests.helpers import not_raises


class TestProcessTime(TestCase):
    def setUp(self):
        self.subject = ProcessTimeFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'time'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.time = "1"

    def test_time_setter_conversion_to_integer(self):
        self.subject.time = "42"
        assert_equal(self.subject.time, 42)
