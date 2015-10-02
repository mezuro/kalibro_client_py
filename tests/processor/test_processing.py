from unittest import TestCase
from nose.tools import assert_equal, assert_true
from mock import patch

from kalibro_client.processor import ProcessTime

from tests.factories import ProcessingFactory, ProcessTimeFactory

from tests.helpers import not_raises


class TestProcessing(TestCase):
    def setUp(self):
        self.subject = ProcessingFactory.build()
        self.process_time = ProcessTimeFactory.build()
        self.process_times = [self.process_time]

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'date'))
        assert_true(hasattr(self.subject, 'repository_id'))
        assert_true(hasattr(self.subject, 'root_module_result_id'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.date = "1"
        self.subject.repository_id = 1
        self.subject.root_module_result_id = 1

    def test_process_times(self):
        process_times_hash = {"process_times": [self.process_time._asdict()]}
        with patch.object(self.subject, 'request', return_value=process_times_hash) as request_mock, \
        patch.object(ProcessTime, 'response_to_objects_array', return_value=self.process_times) as mock:
            response = self.subject.process_times()
            second_response = self.subject.process_times()
            request_mock.assert_called_once_with(action=':id/process_times', params={'id': self.subject.id}, method='get')
            mock.assert_called_once_with(process_times_hash)
            assert_equal(response, self.process_times)
            assert_equal(response, second_response)

    def test_asdict(self):
        dict_ = self.subject._asdict()

        assert_equal(dict_['repository_id'], self.subject.repository_id)
        assert_equal(dict_['date'], self.subject.date)
        assert_equal(dict_['root_module_result_id'], self.subject.root_module_result_id)
