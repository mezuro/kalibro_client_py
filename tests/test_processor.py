from unittest import TestCase, skip
from kalibro_client.processor import Project, Repository
from kalibro_client.processor.base import Base
import kalibro_client

from nose.tools import assert_equal, assert_true

from mock import patch
from factories import ProjectFactory, RepositoryFactory, KalibroModuleFactory

import dateutil

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
        self.date = dateutil.parser.parse("2015-07-05T22:16:18+00:00")

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'period'))
        assert_true(hasattr(self.subject, 'project_id'))
        assert_true(hasattr(self.subject, 'kalibro_configuration_id'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.period = None
        self.subject.project_id = None
        self.subject.kalibro_configuration_id = None

    def test_process(self):
        with patch.object(Repository, 'request') as repository_request:
            self.subject.process()
            repository_request.assert_called_once_with(action='/process', params={'id': self.subject.id}, method='get')

    def test_cancel_processing(self):
        with patch.object(Repository, 'request') as repository_request:
            self.subject.cancel_processing_of_a_repository()
            repository_request.assert_called_once_with(action=':id/cancel_process', params={'id': self.subject.id}, method='get')

    @skip
    def test_processing(self):
        pass

    @skip
    def test_processing_with_date(self):
        pass

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

    @skip
    def test_last_ready_processing(self):
        pass

    @skip
    def test_first_processing(self):
        pass

    @skip
    def test_last_processing(self):
        pass

    @skip
    def test_first_processing_after(self):
        pass

    @skip
    def test_last_processing_before(self):
        pass

    @skip
    def test_branches(self):
        pass
