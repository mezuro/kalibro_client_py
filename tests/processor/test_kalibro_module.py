from unittest import TestCase
from nose.tools import assert_equal, assert_true

from tests.factories import KalibroModuleFactory

from tests.helpers import not_raises


class TestKalibroModule(TestCase):
    def setUp(self):
        self.subject = KalibroModuleFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'name'))

        long_name = "test.name"
        self.subject.long_name = long_name
        assert_equal(self.subject.name, long_name.split("."))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        long_name = "test.name"
        self.subject.name = long_name
        assert_equal(self.subject.long_name, long_name)

        name = ["test", "name"]
        self.subject.name = name
        assert_equal(self.subject.long_name, ".".join(name))

    def test_short_name(self):
        name = ["test", "name"]
        self.subject.name = name
        assert_equal(self.subject.short_name, name[-1])

    def test_granularity(self):
        assert_equal(self.subject.granularity, self.subject.granlrty)
