from unittest import TestCase
from kalibro_client.processor import Project, Repository, ProcessTime
from kalibro_client.processor.base import Base
import kalibro_client

from nose.tools import assert_equal, assert_true

from mock import patch
from factories import ProjectFactory, RepositoryFactory, KalibroModuleFactory,\
    ProcessingFactory

import dateutil

from .helpers import not_raises

from factories import ProjectFactory, RepositoryFactory, ProcessTimeFactory

from .helpers import not_raises

class TestProcessorBase(TestCase):
    @patch('kalibro_client.config')
    def test_service_address(self, kalibro_client_config):
        kalibro_client_config.return_value = kalibro_client.DEFAULT_CONFIG

        assert_equal(Base.service_address(), kalibro_client.DEFAULT_CONFIG['processor_address'])
        kalibro_client_config.assert_called_once()


class TestProject(TestCase):
    def setUp(self):
        self.project = ProjectFactory.build()
        self.project.id = 1
        self.repository = RepositoryFactory.build()
        self.repositories = [self.repository]

    def test_repositories(self):
        repositories_hash = {"repositories": [self.repository._asdict()]}
        with patch.object(Project, 'request', return_value=repositories_hash) as request_mock, \
        patch.object(Repository, 'response_to_objects_array', return_value=self.repositories) as mock:
            self.project.repositories()
            request_mock.assert_called_once_with("1/repositories", method='get')
            mock.assert_called_once_with(repositories_hash)

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


class TestRepository(TestCase):
    def setUp(self):
        self.subject = RepositoryFactory.build()
        self.date_str = "2015-07-05T22:16:18+00:00"
        self.date = dateutil.parser.parse(self.date_str)

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'period'))
        assert_true(hasattr(self.subject, 'project_id'))
        assert_true(hasattr(self.subject, 'kalibro_configuration_id'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.period = None
        self.subject.project_id = None
        self.subject.kalibro_configuration_id = None

    def test_repository_types(self):
        response = {"types": ["GIT", "SVN"]}
        with patch.object(Repository, 'request', return_value=response) as repository_request:
            assert_equal(self.subject.repository_types(), response["types"])
            repository_request.assert_called_once_with(action='/types', params={}, method='get')

    def test_repository_types_with_none(self):
        response = {"types": None}
        with patch.object(Repository, 'request', return_value=response) as repository_request:
            assert_equal(self.subject.repository_types(), [])
            repository_request.assert_called_once_with(action='/types', params={}, method='get')

    def test_repositories_of(self):
        response = {"repositories": [self.subject._asdict()]}
        with patch.object(Repository, 'request', return_value=response) as request_mock, \
            patch.object(Repository, 'response_to_objects_array', return_value=[self.subject]) as response_to_array_mock:
            repositories = Repository.repositories_of(self.subject.project_id)
            request_mock.assert_called_once_with(
                action='',
                params={'id': self.subject.project_id},
                method='get',
                prefix='projects/:id')
            response_to_array_mock.assert_called_once_with(response)
            assert_equal(repositories, [self.subject])

    def test_process(self):
        with patch.object(Repository, 'request') as repository_request:
            self.subject.process()
            repository_request.assert_called_once_with(action='/process', params={'id': self.subject.id}, method='get')

    def test_cancel_processing(self):
        with patch.object(Repository, 'request') as repository_request:
            self.subject.cancel_processing_of_a_repository()
            repository_request.assert_called_once_with(action=':id/cancel_process', params={'id': self.subject.id}, method='get')

    def test_processing_with_ready_processing(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_ready_processing', return_value=True) as has_ready_processing_request, \
             patch.object(Repository, 'last_ready_processing', return_value=processing) as last_ready_processing_request:
            self.subject.processing()
            has_ready_processing_request.assert_called_once()
            last_ready_processing_request.assert_called_once()

    def test_processing_without_ready_processing(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_ready_processing', return_value=False) as has_ready_processing_request, \
             patch.object(Repository, 'last_processing', return_value=processing) as last_processing_request:
            self.subject.processing()
            has_ready_processing_request.assert_called_once()
            last_processing_request.assert_called_once()

    def test_processing_with_date_as_string_after(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=True) as has_processing_after_request, \
             patch.object(Repository, 'first_processing_after', return_value=processing) as first_processing_after_request:
            self.subject.processing_with_date(self.date_str)
            has_processing_after_request.assert_called_once_with(self.date)
            first_processing_after_request.assert_called_once_with(self.date)

    def test_processing_with_date_as_string_before(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=False) as has_processing_after_request, \
             patch.object(Repository, 'has_processing_before', return_value=True) as has_processing_before_request, \
             patch.object(Repository, 'last_processing_before', return_value=processing) as last_processing_before_request:
            self.subject.processing_with_date(self.date_str)
            has_processing_after_request.assert_called_once_with(self.date)
            has_processing_before_request.assert_called_once_with(self.date)
            last_processing_before_request.assert_called_once_with(self.date)

    def test_processing_with_date_as_string(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=False) as has_processing_after_request, \
             patch.object(Repository, 'has_processing_before', return_value=False) as has_processing_before_request:
            assert_equal(self.subject.processing_with_date(self.date_str), None)
            has_processing_after_request.assert_called_once_with(self.date)
            has_processing_before_request.assert_called_once_with(self.date)


    def test_processing_with_date_after(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=True) as has_processing_after_request, \
             patch.object(Repository, 'first_processing_after', return_value=processing) as first_processing_after_request:
            self.subject.processing_with_date(self.date)
            has_processing_after_request.assert_called_once_with(self.date)
            first_processing_after_request.assert_called_once_with(self.date)

    def test_processing_with_date_before(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=False) as has_processing_after_request, \
             patch.object(Repository, 'has_processing_before', return_value=True) as has_processing_before_request, \
             patch.object(Repository, 'last_processing_before', return_value=processing) as last_processing_before_request:
            self.subject.processing_with_date(self.date)
            has_processing_after_request.assert_called_once_with(self.date)
            has_processing_before_request.assert_called_once_with(self.date)
            last_processing_before_request.assert_called_once_with(self.date)

    def test_processing_with_date(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=False) as has_processing_after_request, \
             patch.object(Repository, 'has_processing_before', return_value=False) as has_processing_before_request:
            assert_equal(self.subject.processing_with_date(self.date), None)
            has_processing_after_request.assert_called_once_with(self.date)
            has_processing_before_request.assert_called_once_with(self.date)

    def test_has_processing(self):
        has_processing_hash = {'has_processing': True}
        with patch.object(Repository, 'request',
                          return_value=has_processing_hash) as repository_request:
            response = self.subject.has_processing()
            repository_request.assert_called_once_with(':id/has_processing', params={'id': self.subject.id}, method='get')
            assert_equal(response, True)

    def test_has_ready_processing(self):
        has_ready_processing_hash = {'has_ready_processing': True}
        with patch.object(Repository, 'request',
                          return_value=has_ready_processing_hash) as repository_request:
            response = self.subject.has_ready_processing()
            repository_request.assert_called_once_with(':id/has_ready_processing', params={'id': self.subject.id}, method='get')
            assert_equal(response, True)

    def test_has_processing_after(self):
        has_processing_after = {'has_processing_in_time': True}
        with patch.object(Repository, 'request',
                          return_value=has_processing_after) as repository_request:
            response = self.subject.has_processing_after(self.date)
            repository_request.assert_called_once_with(':id/has_processing/after', params={'id': self.subject.id, 'date': self.date})
            assert_equal(response, True)

    def test_has_processing_before(self):
        has_processing_before = {'has_processing_in_time': True}
        with patch.object(Repository, 'request',
                          return_value=has_processing_before) as repository_request:
            response = self.subject.has_processing_before(self.date)
            repository_request.assert_called_once_with(':id/has_processing/before', params={'id': self.subject.id, 'date': self.date})
            assert_equal(response, True)

    def test_last_processing_state(self):
        processing_state_hash = {'processing_state': 'READY'}
        with patch.object(Repository, 'request',
                          return_value=processing_state_hash) as repository_request:
            response = self.subject.last_processing_state()
            repository_request.assert_called_once_with(':id/last_processing_state', params={'id': self.subject.id}, method='get')
            assert_equal(response, 'READY')

    def test_last_ready_processing(self):
        processing = ProcessingFactory.build()
        processing_hash = {'last_ready_processing': processing._asdict()}
        with patch.object(Repository, 'request',
                          return_value=processing_hash) as repository_request:
            response = self.subject.last_ready_processing()
            repository_request.assert_called_once_with(':id/last_ready_processing', params={'id': self.subject.id}, method='get')
            assert_equal(response, processing)

    def test_first_processing(self):
        processing = ProcessingFactory.build()
        processing_hash = {'processing': processing._asdict()}

        with patch.object(Repository, 'request',
                          return_value=processing_hash) as repository_request:
            response = self.subject.first_processing()
            repository_request.assert_called_once_with(':id/first_processing', params={'id': self.subject.id})
            assert_equal(response, processing)

    def test_last_processing(self):
        processing = ProcessingFactory.build()
        processing_hash = {'processing': processing._asdict()}

        with patch.object(Repository, 'request',
                          return_value=processing_hash) as repository_request:
            response = self.subject.last_processing()
            repository_request.assert_called_once_with(':id/last_processing', params={'id': self.subject.id})
            assert_equal(response, processing)

    def test_first_processing_after(self):
        processing = ProcessingFactory.build()
        processing_hash = {'processing': processing._asdict()}

        with patch.object(Repository, 'request',
                          return_value=processing_hash) as repository_request:
            response = self.subject.first_processing_after(self.date)
            repository_request.assert_called_once_with(':id/first_processing/after', params={'id': self.subject.id, 'date': self.date})
            assert_equal(response, processing)

    def test_last_processing_before(self):
        processing = ProcessingFactory.build()
        processing_hash = {'processing': processing._asdict()}

        with patch.object(Repository, 'request',
                          return_value=processing_hash) as repository_request:
            response = self.subject.last_processing_before(self.date)
            repository_request.assert_called_once_with(':id/last_processing/before', params={'id': self.subject.id, 'date': self.date})
            assert_equal(response, processing)

    def test_branches(self):
        branches = {'branches': ['master', 'stable']}
        url = 'https://github.com/mezuro/kalibro_client_py.git'
        scm_type = 'GIT'

        with patch.object(Repository, 'request',
                          return_value=branches) as repository_request:
            Repository.branches(url, scm_type)
            repository_request.assert_called_once_with("/branches", {'url': url, 'scm_type': scm_type})
