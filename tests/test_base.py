from mock import Mock, patch
from nose.tools import assert_equal, raises

from kalibro_client.base import Configuration, Base

class TestConfiguration(object):
    def setUp(self):
        self.host = 'localhost'
        self.port = '8000'
        self.configuration = Configuration(self.host, self.port)

    def test_init(self):
        assert_equal(self.configuration.host, self.host)
        assert_equal(self.configuration.port, self.port)

    def test_service_address(self):
        assert_equal(self.configuration.service_address,
                     "{}:{}".format(self.host, self.port))

    def test_from_options(self):
        # This kind of assert works just because configuration is a namedtuple
        assert_equal(Configuration.from_options({'host': self.host,
                                                 'port': self.port}),
                     self.configuration)

class TestBase(object):
    def setUp(self):
        self.attributes = {'id': 1, 'name': 'A random Project',
                           'description': 'A real example Project'}
        self.base = Base(self.attributes)

    def test_init(self):
        assert_equal(self.base.id, 1)
        assert_equal(self.base.name, 'A random Project')
        assert_equal(self.base.description, 'A real example Project')

    @raises(NotImplementedError)
    def test_entity_name(self):
        self.base.entity_name()

    @patch('requests.request')
    def test_request(self, requests_request):
        self.base.endpoint = Mock(return_value="base")

        response_mock = Mock()
        response_mock.json = Mock(return_value=self.attributes)
        requests_request.return_value = response_mock

        assert_equal(self.base.request("find", method='get'), self.attributes)
        requests_request.assert_called_once_with('get', "/base/find",
                                                 params=None)
        response_mock.json.assert_called_with()

    @patch('requests.request')
    def test_request_with_prefix(self, requests_request):
        self.base.endpoint = Mock(return_value="base")

        response_mock = Mock()
        response_mock.json = Mock(return_value=self.attributes)
        requests_request.return_value = response_mock

        assert_equal(self.base.request("find", method='get', prefix='prefix'),
                     self.attributes)
        requests_request.assert_called_once_with('get', "/prefix/base/find",
                                                 params=None)
        response_mock.json.assert_called_with()

    @patch('requests.request')
    def test_request_with_default_method(self, requests_request):
        self.base.endpoint = Mock(return_value="base")

        response_mock = Mock()
        response_mock.json = Mock(return_value=self.attributes)
        requests_request.return_value = response_mock

        assert_equal(self.base.request("create"), self.attributes)
        requests_request.assert_called_once_with('post', "/base/create",
                                                 params=None)
        response_mock.json.assert_called_with()

    @Base.entity_name_decorator()
    class Entity(Base):
        pass

    class EntitySubclass(Entity):
        pass

    @Base.entity_name_decorator()
    class CompositeEntity(Base):
        pass

    def test_entity_name_decorator(self):
        entity = self.Entity(dict())
        assert_equal(
            entity.entity_name(), "entity",
            "Deriving classes with the decorator should be automatically named")

    def test_entity_name_decorator_subclass(self):
        entity_sub = self.EntitySubclass(dict())
        assert_equal(
            entity_sub.entity_name(), "entity",
            "Deriving classes without the decorator should keep the name of "
            "their superclass")

    def test_entity_name_decorator_composite(self):
        composite_entity = self.CompositeEntity(dict())
        assert_equal(
            composite_entity.entity_name(), "composite_entity",
            "Entity name should be underscored and lowercased")

    @raises(NotImplementedError)
    def test_endpoint_base(self):
        self.base.endpoint()

    def test_endpoint(self):
        cases = {
            'repository': 'repositories',
            'project': 'projects',
            'processing': 'processings',
            'process_time': 'process_times'
        }

        for (singular, plural) in cases.items():
            with patch.object(self.base.__class__, 'entity_name',
                              return_value=singular):
                assert_equal(self.base.endpoint(), plural)

        assert_equal(self.CompositeEntity(dict()).endpoint(),
                     "composite_entities")