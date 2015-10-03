import json
from unittest import TestCase
from nose.tools import assert_equal, assert_true, raises
from mock import Mock, patch

from kalibro_client.base import RequestMethods


class TestRequestMethods(TestCase):

    def setUp(self):
        self.attributes = {'name': 'A random Project',
                           'description': 'A real example Project'}
        self.subject = RequestMethods()
        self.nulldata = json.dumps(None)  # request method always calls json.dumps
        self.headers = {'Content-Type': 'application/json'}
        self.json_dumps_attributes = json.dumps(self.attributes)

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

    @raises(NotImplementedError)
    def test_entity_name(self):
        self.subject.entity_name()

    @patch('requests.request')
    def test_request(self, requests_request):
        with patch.object(type(self.subject), 'endpoint', return_value="request_methods") as mock_endpoint, \
            patch.object(type(self.subject), 'service_address',
                         return_value="http://request_methods:8000") as mock_service_address:
            response_mock = Mock()
            response_mock.json = Mock(return_value=self.attributes)
            requests_request.return_value = response_mock

            assert_equal(self.subject.request("find", method='get'), self.attributes)
            requests_request.assert_called_once_with('get', "http://request_methods:8000/request_methods/find",
                                                     data=self.nulldata, headers=self.headers)
            mock_endpoint.assert_called_once()
            mock_service_address.assert_called_once()
            response_mock.json.assert_called_with()

    @patch('requests.request')
    def test_request_with_prefix(self, requests_request):
        with patch.object(type(self.subject), 'endpoint', return_value="request_methods") as mock_endpoint, \
             patch.object(type(self.subject), 'service_address', return_value="http://request_methods:8000") as mock_service_address:

            response_mock = Mock()
            response_mock.json = Mock(return_value=self.attributes)
            requests_request.return_value = response_mock

            assert_equal(self.subject.request("find", method='get', prefix='prefix'),
                         self.attributes)
            requests_request.assert_called_once_with('get', "http://request_methods:8000/prefix/request_methods/find",
                                                     data=self.nulldata, headers=self.headers)
            response_mock.json.assert_called_with()
            mock_endpoint.assert_called_once()
            mock_service_address.assert_called_once()

    @patch('requests.request')
    def test_request_with_default_method(self, requests_request):
        with patch.object(type(self.subject), 'endpoint', return_value="request_methods") as mock_endpoint, \
             patch.object(type(self.subject), 'service_address', return_value="http://request_methods:8000") as mock_service_address:

            response_mock = Mock()
            response_mock.json = Mock(return_value=self.attributes)
            requests_request.return_value = response_mock

            assert_equal(self.subject.request("create"), self.attributes)
            requests_request.assert_called_once_with('post', "http://request_methods:8000/request_methods/create",
                                                     data=self.nulldata, headers=self.headers)
            response_mock.json.assert_called_with()
            mock_endpoint.assert_called_once()
            mock_service_address.assert_called_once()

    @patch('json.dumps')
    @patch('requests.request')
    def test_request_with_parameters(self, requests_request, json_dumps):
        with patch.object(type(self.subject), 'endpoint', return_value="request_methods") as mock_endpoint, \
             patch.object(type(self.subject), 'service_address', return_value="http://request_methods:8000") as mock_service_address:
            response_mock = Mock()
            response_mock.json = Mock(return_value=self.attributes)
            requests_request.return_value = response_mock
            json_dumps.return_value = self.json_dumps_attributes

            assert_equal(self.subject.request("create", params=self.attributes), self.attributes)
            json_dumps.assert_called_once_with(self.attributes)
            requests_request.assert_called_once_with('post', "http://request_methods:8000/request_methods/create",
                                                     data=self.json_dumps_attributes, headers=self.headers)
            response_mock.json.assert_called_with()
            mock_endpoint.assert_called_once()
            mock_service_address.assert_called_once()

    @patch('json.dumps')
    @patch('requests.request')
    def test_request_with_id_parameter(self, requests_request, json_dumps):
        with patch.object(type(self.subject), 'endpoint', return_value="request_methods") as mock_endpoint, \
             patch.object(type(self.subject), 'service_address', return_value="http://request_methods:8000") as mock_service_address:
            response_mock = Mock()
            response_mock.json = Mock(return_value=self.attributes)
            requests_request.return_value = response_mock

            attributes = {'id': 42}
            self.subject.request(":id/something", params=attributes)
            json_dumps.assert_called_once_with({})
            requests_request.assert_called_once_with('post', "http://request_methods:8000/request_methods/42/something",
                                                     data=json.dumps({}), headers=self.headers)
            response_mock.json.assert_called_with()
            mock_endpoint.assert_called_once()


