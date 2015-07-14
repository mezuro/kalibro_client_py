import json
from unittest import TestCase

from mock import Mock, patch, create_autospec
from nose.tools import assert_equal, assert_true, assert_raises_regexp, raises
import dateutil.parser

from kalibro_client.base import Base, attributes_class_constructor, entity_name_decorator
from kalibro_client.errors import KalibroClientSaveError

from .helpers import not_raises

class Derived(attributes_class_constructor('DerivedAttr', ('name', 'description'), identity=False), Base):
    pass

@entity_name_decorator
class CompositeEntity(Base):
    pass


class TestBase(TestCase):
    def setUp(self):
        self.attributes = {'name': 'A random Project',
                           'description': 'A real example Project'}
        self.base = Derived(**self.attributes)
        self.headers = {'Content-Type': 'application/json'}
        self.nulldata = json.dumps(None)  # request method always calls json.dumps
        self.json_dumps_attributes = json.dumps(self.attributes)

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
                                                 data=self.nulldata, headers=self.headers)
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
                                                 data=self.nulldata, headers=self.headers)
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
                                                 data=self.nulldata, headers=self.headers)
        response_mock.json.assert_called_with()

    @patch('json.dumps')
    @patch('requests.request')
    def test_request_with_parameters(self, requests_request, json_dumps):
        self.base.endpoint = Mock(return_value="base")
        self.base.service_address = Mock(return_value="http://base:8000")

        response_mock = Mock()
        response_mock.json = Mock(return_value=self.attributes)
        requests_request.return_value = response_mock
        json_dumps.return_value = self.json_dumps_attributes

        assert_equal(self.base.request("create", params=self.attributes), self.attributes)
        json_dumps.assert_called_once_with(self.attributes)
        requests_request.assert_called_once_with('post', "http://base:8000/base/create",
                                                 data=self.json_dumps_attributes, headers=self.headers)
        response_mock.json.assert_called_with()

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

        assert_equal(CompositeEntity().endpoint(),
                     "composite_entities")

    @entity_name_decorator
    class IdentifiedBase(attributes_class_constructor('Identified', ('attribute')), Base):
        pass

    @not_raises(KalibroClientSaveError)
    def test_successful_save(self):
        subject = self.IdentifiedBase(attribute='test')

        id = 42
        date = dateutil.parser.parse("2015-07-05T22:16:18+00:00")

        successful_response = {'identified_base': {'id': str(id),
                                                   'created_at': date.isoformat(),
                                                   'updated_at': date.isoformat()}}
        subject.request = create_autospec(subject.request, return_value=successful_response)

        subject.save()

        subject.request.assert_called_with('', {subject.entity_name() : subject._asdict()})
        assert_equal(subject.id, id)
        assert_equal(subject.created_at, date)
        assert_equal(subject.updated_at, date)

    @raises(KalibroClientSaveError)
    def test_unsuccessful_save(self):
        subject = self.IdentifiedBase(attribute='test')

        unsuccessful_response = {'errors': ['A string with an error']}
        subject.request = create_autospec(subject.request, return_value=unsuccessful_response)

        subject.save()

        subject.request.assert_called_with('', {subject.entity_name() : subject._asdict()})

    @not_raises(KalibroClientSaveError)
    def test_successful_update(self):
        date = dateutil.parser.parse("2015-07-05T22:16:18+00:00")
        updated_date = dateutil.parser.parse("2020-07-05T22:16:18+00:00")
        new_attribute_value = 'new_value'

        subject = self.IdentifiedBase(id=42, created_at=date, updated_at=date, attribute='test')

        request_params = {subject.entity_name(): subject._asdict()}
        request_params['id'] = str(subject.id)
        request_params[subject.entity_name()]['attribute'] = new_attribute_value

        successful_response = {'identified_base': {'id': str(subject.id),
                                                   'created_at': date.isoformat(),
                                                   'updated_at': updated_date.isoformat(),
                                                   'attribute': new_attribute_value}}
        subject.request = create_autospec(subject.request, return_value=successful_response)

        subject.update(attribute=new_attribute_value)

        subject.request.assert_called_with(str(subject.id), request_params, method='put')

        assert_equal(subject.id, 42)
        assert_equal(subject.created_at, date)
        assert_equal(subject.updated_at, updated_date)
        assert_equal(subject.attribute, new_attribute_value)

    def test_unsuccessful_update_without_id(self):
        subject = self.IdentifiedBase(id=None, attribute='test')
        subject.request = create_autospec(subject.request,
            side_effect=AssertionError("Request should not be called for update without id"))

        with assert_raises_regexp(KalibroClientSaveError,
                                  "Cannot update a record that is not saved."):
            subject.update(attribute='new value')

    @raises(KalibroClientSaveError)
    def test_unsuccessful_update(self):
        subject = self.IdentifiedBase(id=42, attribute='test')
        unsuccessful_response = {'errors': ['A string with an error']}

        subject.request = create_autospec(subject.request, return_value=unsuccessful_response)

        subject.update(attribute='new_value')

    def test_is_valid_field(self):
        assert_true(self.IdentifiedBase._is_valid_field('attribute'))
        assert_true(not self.IdentifiedBase._is_valid_field('invalid'))
        assert_true(not self.IdentifiedBase._is_valid_field('errors'))


class TestsEntityNameDecorator(TestCase):
    @entity_name_decorator
    class Entity(Base):
        def __init__(self):
            pass

    class EntitySubclass(Entity):
        pass


    def test_decorator(self):
        entity = self.Entity()
        assert_equal(
            entity.entity_name(), "entity",
            "Deriving classes with the decorator should be automatically named")

    def test_decorator_with_subclass(self):
        entity_sub = self.EntitySubclass()
        assert_equal(
            entity_sub.entity_name(), "entity",
            "Deriving classes without the decorator should keep the name of "
            "their superclass")

    def test_decorator_with_composite_name(self):
        composite_entity = CompositeEntity()
        assert_equal(
            composite_entity.entity_name(), "composite_entity",
            "Entity name should be underscored and lowercased")

class TestAttributesClassConstructor(TestCase):
    class Identified(attributes_class_constructor('IdentifiedAttr', ())):
        pass

    def setUp(self):
        self.identified = self.Identified()

    def test_properties_getters(self):
        assert_true(hasattr(self.identified, 'id'))
        assert_true(hasattr(self.identified, 'created_at'))
        assert_true(hasattr(self.identified, 'updated_at'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.identified.id = None
        self.identified.created_at = None
        self.identified.updated_at = None

    @not_raises(ValueError)
    def test_id_setter(self):
        self.identified.id = 10
        self.identified.id = "10"

    @raises(ValueError)
    def test_id_setter_invalid(self):
        self.identified.id = "wrong"

    @not_raises(ValueError)
    def test_created_at_setter(self):
        # ISO8601 format
        date_str = "2015-07-05T22:16:18+00:00"
        self.identified.created_at = date_str

        date_obj = dateutil.parser.parse(date_str)
        self.identified.created_at = date_obj

    @raises(ValueError)
    def test_created_at_setter_invalid(self):
        self.identified.created_at = "wrong"

    @not_raises(ValueError)
    def test_updated_at_setter(self):
        # ISO8601 format
        date_str = "2015-07-05T22:16:18+00:00"
        self.identified.updated_at = date_str

        date_obj = dateutil.parser.parse(date_str)
        self.identified.updated_at = date_obj

    @raises(ValueError)
    def test_updated_at_setter_invalid(self):
        self.identified.updated_at = "wrong"
