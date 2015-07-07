from mock import Mock, patch
from nose.tools import assert_equal, raises, assert_true

from kalibro_client.base import Base, attributes_class_constructor

#@Base.entity_name_decorator()
class Derived(attributes_class_constructor('DerivedAttr', ('name', 'description'), False), Base):
    pass

class TestBase(object):
    def setUp(self):
        self.attributes = {'name': 'A random Project',
                           'description': 'A real example Project'}
        self.base = Derived(**self.attributes)

    def test_init(self):
        assert_equal(self.base.name, 'A random Project')
        assert_equal(self.base.description, 'A real example Project')

    @raises(NotImplementedError)
    def test_entity_name(self):
        self.base.entity_name()

    @raises(NotImplementedError)
    def test_service_address(self):
        self.base.service_address()

    @patch('requests.request')
    def test_request(self, requests_request):
        self.base.endpoint = Mock(return_value="base")
        self.base.service_address = Mock(return_value="http://base:8000")

        response_mock = Mock()
        response_mock.json = Mock(return_value=self.attributes)
        requests_request.return_value = response_mock

        assert_equal(self.base.request("find", method='get'), self.attributes)
        requests_request.assert_called_once_with('get', "http://base:8000/base/find",
                                                 params=None)
        response_mock.json.assert_called_with()

    @patch('requests.request')
    def test_request_with_prefix(self, requests_request):
        self.base.endpoint = Mock(return_value="base")
        self.base.service_address = Mock(return_value="http://base:8000")

        response_mock = Mock()
        response_mock.json = Mock(return_value=self.attributes)
        requests_request.return_value = response_mock

        assert_equal(self.base.request("find", method='get', prefix='prefix'),
                     self.attributes)
        requests_request.assert_called_once_with('get', "http://base:8000/prefix/base/find",
                                                 params=None)
        response_mock.json.assert_called_with()

    @patch('requests.request')
    def test_request_with_default_method(self, requests_request):
        self.base.endpoint = Mock(return_value="base")
        self.base.service_address = Mock(return_value="http://base:8000")

        response_mock = Mock()
        response_mock.json = Mock(return_value=self.attributes)
        requests_request.return_value = response_mock

        assert_equal(self.base.request("create"), self.attributes)
        requests_request.assert_called_once_with('post', "http://base:8000/base/create",
                                                 params=None)
        response_mock.json.assert_called_with()

    @Base.entity_name_decorator()
    class Entity(Base):
        def __init__(self):
            pass

    class EntitySubclass(Entity):
        pass

    @Base.entity_name_decorator()
    class CompositeEntity(Base):
        pass

    def test_entity_name_decorator(self):
        entity = self.Entity()
        assert_equal(
            entity.entity_name(), "entity",
            "Deriving classes with the decorator should be automatically named")

    def test_entity_name_decorator_subclass(self):
        entity_sub = self.EntitySubclass()
        assert_equal(
            entity_sub.entity_name(), "entity",
            "Deriving classes without the decorator should keep the name of "
            "their superclass")

    def test_entity_name_decorator_composite(self):
        composite_entity = self.CompositeEntity()
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

        assert_equal(self.CompositeEntity().endpoint(),
                     "composite_entities")

    class Identified(attributes_class_constructor('IdentifiedAttr', (), True)):
        pass

    def test_identity_mixin_attributes(self):
        identified = self.Identified()

        assert_true(hasattr(identified, 'id'))
        assert_true(hasattr(identified, 'created_at'))
        assert_true(hasattr(identified, 'updated_at'))

        #assert_true(hasattr(identified, 'id='))
        #assert_true(hasattr(identified, 'created_at='))
        #assert_true(hasattr(identified, 'updated_at='))