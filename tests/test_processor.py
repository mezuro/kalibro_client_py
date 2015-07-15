from unittest import TestCase
from kalibro_client.processor import Project, Repository

from mock import patch
from factories import ProjectFactory, RepositoryFactory


class TestProcessor(TestCase):

    def setUp(self):
        self.project = ProjectFactory.build()
        self.project.id = 1
        self.repository = RepositoryFactory.build()
        self.repositories = [self.repository]

    def test_repositories(self):
        repositories_hash = {"repositories": [self.repository._as_dict()]}
        with patch.object(Project, 'request', return_value=repositories_hash) as request_mock, \
        patch.object(Repository, 'response_to_objects_array', return_value=self.repositories) as mock:
            self.project.repositories()
            request_mock.assert_called_once_with("1/repositories", method='get')
            mock.assert_called_once_with(repositories_hash)
