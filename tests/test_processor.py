from unittest import TestCase
from kalibro_client.processor import Project, Repository
from kalibro_client.processor.base import Base
import kalibro_client

from nose.tools import assert_equal

from mock import Mock, patch
from factories import ProjectFactory, RepositoryFactory

class TestProcessorBase(TestCase):
    @patch('kalibro_client.config')
    def test_service_address(self, kalibro_client_config):
        kalibro_client_config.return_value = kalibro_client.DEFAULT_CONFIG

        assert_equal(Base.service_address(), kalibro_client.DEFAULT_CONFIG['processor_address'])
        kalibro_client_config.assert_called_once()

class TestProcessor(TestCase):

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
