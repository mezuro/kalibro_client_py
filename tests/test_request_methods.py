from unittest import TestCase
from nose.tools import assert_equal, assert_true, raises
from mock import patch

from kalibro_client.base import RequestMethods


class TestRequestMethods(TestCase):

    def setUp(self):
        self.subject = RequestMethods()

    def test_prefixes(self):
        assert_equal(self.subject.save_prefix(), "")
        assert_equal(self.subject.update_prefix(), "")
        assert_equal(self.subject.delete_prefix(), "")

    def test_endpoint(self):
        cases = {
            'repository': 'repositories',
            'project': 'projects',
            'processing': 'processings',
            'process_time': 'process_times'
        }

        for (singular, plural) in cases.items():
            with patch.object(self.subject.__class__, 'entity_name',
                              return_value=singular):
                assert_equal(self.subject.endpoint(), plural)

    @raises(NotImplementedError)
    def test_service_address(self):
        self.subject.service_address()
