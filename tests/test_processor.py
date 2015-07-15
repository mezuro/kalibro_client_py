from unittest import TestCase
from kalibro_client.processor import Project, Repository
from kalibro_client.processor.base import Base
import kalibro_client

from nose.tools import assert_equal, assert_true

from mock import patch
from factories import ProjectFactory, RepositoryFactory, KalibroModuleFactory

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

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'period'))
        assert_true(hasattr(self.subject, 'project_id'))
        assert_true(hasattr(self.subject, 'kalibro_configuration_id'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.period = None
        self.subject.project_id = None
        self.subject.kalibro_configuration_id = None
