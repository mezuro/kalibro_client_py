import json
from unittest import TestCase

from mock import Mock, patch, create_autospec
from nose.tools import assert_equal, assert_true, assert_raises_regexp, raises
import dateutil.parser

from kalibro_client.base import BaseCRUD, attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.errors import KalibroClientSaveError, KalibroClientDeleteError, \
    KalibroClientNotFoundError

from .helpers import not_raises


class Derived(attributes_class_constructor('DerivedAttr',
                                           ('name', 'description'),
                                           identity=False), BaseCRUD):
    pass


@entity_name_decorator
class DerivedWithEntityName(attributes_class_constructor('DerivedAttr', ('name', 'description'), identity=False), BaseCRUD):
    pass

@entity_name_decorator
class CompositeEntity(BaseCRUD):
    pass


@entity_name_decorator
class IdentifiedBase(attributes_class_constructor('Identified',
                                                  ('attribute')), BaseCRUD):
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
        BaseCRUD.service_address()

    @patch('requests.request')
    def test_request(self, requests_request):
        with patch.object(type(self.base), 'endpoint', return_value="base") as mock_endpoint, \
            patch.object(type(self.base), 'service_address', return_value="http://base:8000") as mock_service_address:
            response_mock = Mock()
            response_mock.json = Mock(return_value=self.attributes)
            requests_request.return_value = response_mock

            assert_equal(self.base.request("find", method='get'), self.attributes)
            requests_request.assert_called_once_with('get', "http://base:8000/base/find",
                                                     data=self.nulldata, headers=self.headers)
            mock_endpoint.assert_called_once()
            mock_service_address.assert_called_once()
            response_mock.json.assert_called_with()

    @patch('requests.request')
    def test_request_with_prefix(self, requests_request):
        with patch.object(type(self.base), 'endpoint', return_value="base") as mock_endpoint, \
            patch.object(type(self.base), 'service_address', return_value="http://base:8000") as mock_service_address:
            response_mock = Mock()
            response_mock.json = Mock(return_value=self.attributes)
            requests_request.return_value = response_mock

            assert_equal(self.base.request("find", method='get', prefix='prefix'),
                         self.attributes)
            requests_request.assert_called_once_with('get', "http://base:8000/prefix/base/find",
                                                     data=self.nulldata, headers=self.headers)
            response_mock.json.assert_called_with()
            mock_endpoint.assert_called_once()
            mock_service_address.assert_called_once()

    @patch('requests.request')
    def test_request_with_default_method(self, requests_request):
        with patch.object(type(self.base), 'endpoint', return_value="base") as mock_endpoint, \
            patch.object(type(self.base), 'service_address', return_value="http://base:8000") as mock_service_address:

            response_mock = Mock()
            response_mock.json = Mock(return_value=self.attributes)
            requests_request.return_value = response_mock

            assert_equal(self.base.request("create"), self.attributes)
            requests_request.assert_called_once_with('post', "http://base:8000/base/create",
                                                     data=self.nulldata, headers=self.headers)
            response_mock.json.assert_called_with()
            mock_endpoint.assert_called_once()
            mock_service_address.assert_called_once()

    @patch('json.dumps')
    @patch('requests.request')
    def test_request_with_parameters(self, requests_request, json_dumps):
        with patch.object(type(self.base), 'endpoint', return_value="base") as mock_endpoint, \
            patch.object(type(self.base), 'service_address', return_value="http://base:8000") as mock_service_address:
            response_mock = Mock()
            response_mock.json = Mock(return_value=self.attributes)
            requests_request.return_value = response_mock
            json_dumps.return_value = self.json_dumps_attributes

            assert_equal(self.base.request("create", params=self.attributes), self.attributes)
            json_dumps.assert_called_once_with(self.attributes)
            requests_request.assert_called_once_with('post', "http://base:8000/base/create",
                                                     data=self.json_dumps_attributes, headers=self.headers)
            response_mock.json.assert_called_with()
            mock_endpoint.assert_called_once()
            mock_service_address.assert_called_once()

    @patch('json.dumps')
    @patch('requests.request')
    def test_request_with_id_parameter(self, requests_request, json_dumps):
        with patch.object(type(self.base), 'endpoint', return_value="base") as mock_endpoint, \
            patch.object(type(self.base), 'service_address', return_value="http://base:8000") as mock_service_address:
            response_mock = Mock()
            response_mock.json = Mock(return_value=self.attributes)
            requests_request.return_value = response_mock

            attributes = {'id': 42}
            self.base.request(":id/something", params=attributes)
            json_dumps.assert_called_once_with({})
            requests_request.assert_called_once_with('post', "http://base:8000/base/42/something",
                                                     data=json.dumps({}), headers=self.headers)
            response_mock.json.assert_called_with()
            mock_endpoint.assert_called_once()

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

    @not_raises(KalibroClientSaveError)
    def test_successful_save(self):
        subject = IdentifiedBase(attribute='test')

        id = 42
        date = dateutil.parser.parse("2015-07-05T22:16:18+00:00")

        successful_response = {'identified_base': {'id': str(id),
                                                   'created_at': date.isoformat(),
                                                   'updated_at': date.isoformat()}}
        subject.request = create_autospec(subject.request, return_value=successful_response)

        subject.save()

        subject.request.assert_called_with(action='', params={subject.entity_name() : subject._asdict()}, prefix=subject.save_prefix())
        assert_equal(subject.id, id)
        assert_equal(subject.created_at, date)
        assert_equal(subject.updated_at, date)

    def test_unsuccessful_update_without_id(self):
        subject = IdentifiedBase(id=None, attribute='test')
        subject.request = create_autospec(subject.request,
            side_effect=AssertionError("Request should not be called for update without id"))

        with assert_raises_regexp(KalibroClientSaveError,
                                  "Cannot update a record that is not saved."):
            subject.update(attribute='new value')


    @raises(KalibroClientSaveError)
    def test_unsuccessful_save(self):
        subject = IdentifiedBase(attribute='test')

        unsuccessful_response = {'errors': ['A string with an error']}
        subject.request = create_autospec(subject.request, return_value=unsuccessful_response)

        subject.save()

        subject.request.assert_called_with('', {subject.entity_name() : subject._asdict()})


    @raises(KalibroClientSaveError)
    def test_unsuccessful_update(self):
        subject = IdentifiedBase(id=42, attribute='test')
        unsuccessful_response = {'errors': ['A string with an error']}

        subject.request = create_autospec(subject.request, return_value=unsuccessful_response)

        subject.update(attribute='new_value')

    def test_is_valid_field(self):
        assert_true(IdentifiedBase._is_valid_field('attribute'))
        assert_true(not IdentifiedBase._is_valid_field('invalid'))
        assert_true(not IdentifiedBase._is_valid_field('errors'))

    def test_all(self):
        hash_array = [{'name': 'fizz', 'description': 'buzz'},
                      {'name': 'zzif', 'description': 'zzub'}]
        response = {'derived': hash_array}
        objects = [Derived('fizz', 'buzz'),
                   Derived('zzif', 'zzub')]
        with patch.object(Derived, 'request', return_value=response) as request_mock, \
             patch.object(Derived, 'response_to_objects_array', return_value=objects) as mock:
            Derived.all()
            request_mock.assert_called_once_with('', method='get')
            mock.assert_called_once_with(response)

    def test_successful_delete(self):
        subject = IdentifiedBase(id=1, attribute='test')
        with patch.object(subject, 'request', return_value={}) as request_mock:
            subject.delete()
            request_mock.assert_called_once_with(action=':id', params={'id':subject.id}, method='delete', prefix=subject.delete_prefix())

    @raises (KalibroClientDeleteError)
    def test_unsuccessful_delete(self):
        subject = IdentifiedBase(id=1, attribute='test')
        with patch.object(subject, 'request', return_value={'errors':'Resource not found'}) as request_mock:
            subject.delete()
            request_mock.assert_called_once_with(action=':id', params={'id':subject.id}, method='delete', prefix=subject.delete_prefix())

    @raises (KalibroClientDeleteError)
    def test_unsuccessful_delete_without_id(self):
        subject = IdentifiedBase(id=None, attribute='test')
        subject.delete()

    def test_response_to_objects_array(self):
        array = [DerivedWithEntityName('fizz', 'buzz'), DerivedWithEntityName('zzif', 'zzub')]
        with patch.object(DerivedWithEntityName, 'array_to_objects_array', return_value=array) as mock:
            hash_array = [{'name': 'fizz', 'description': 'buzz'},
                          {'name': 'zzif', 'description': 'zzub'}]
            response = {'derived_with_entity_names': hash_array}
            DerivedWithEntityName.response_to_objects_array(response)
            mock.assert_called_once_with(hash_array)


    def test_array_to_objects_array(self):
        array = [{'name': 'fizz', 'description': 'buzz'},
                 {'name': 'zzif', 'description': 'zzub'}]
        assert_equal(DerivedWithEntityName.array_to_objects_array(array),
                     [DerivedWithEntityName('fizz', 'buzz'),
                     DerivedWithEntityName('zzif', 'zzub')])

    def test_when_record_exists(self):
        with patch.object(IdentifiedBase, 'request', return_value={'exists': True}) as mock_request:
            exists = IdentifiedBase.exists(42)
            IdentifiedBase.request.assert_called_with(':id/exists',
                                                      params={'id': 42},
                                                      method='get')
            mock_request.assert_called_once()
            assert_true(exists)

    def test_when_record_does_not_exist(self):
        with patch.object(IdentifiedBase, 'request', return_value={'exists': False}) as mock_request:
            exists = IdentifiedBase.exists(42)
            IdentifiedBase.request.assert_called_with(':id/exists',
                                                      params={'id': 42},
                                                      method='get')
            mock_request.assert_called_once()
            assert_true(not exists)

    def test_find_when_it_finds_something(self):
        date_str = dateutil.parser.parse("2015-07-05T22:16:18+00:00")
        subject = IdentifiedBase(id=1, attribute="attributes",
                                 created_at=date_str, updated_at=date_str)
        with patch.object(IdentifiedBase, 'request',
                          return_value={'identified_base': {'id': subject.id,
                                                            'attribute': subject.attribute,
                                                            'created_at': subject.created_at,
                                                            'updated_at': subject.updated_at}}) as mock:
            found_object = IdentifiedBase.find(subject.id)
            assert_equal(subject, found_object)
            mock.assert_called_once_with(":id", params={'id': (subject.id)}, method='get')

    @raises(KalibroClientNotFoundError)
    def test_find_when_it_does_not_find_anything(self):
        date_str = dateutil.parser.parse("2015-07-05T22:16:18+00:00")
        subject = IdentifiedBase(id=1, attribute="attributes",
                                 created_at=date_str, updated_at=date_str)
        with patch.object(IdentifiedBase, 'request',
                          return_value={'errors': ["Couldn't find object"]}) as mock:
            IdentifiedBase.find(subject.id)
            mock.assert_called_once_with(":id", params={'id': (subject.id)}, method='get')


class TestsEntityNameDecorator(TestCase):
    @entity_name_decorator
    class Entity(BaseCRUD):
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


class TestSuccessfulUpdates(TestCase):

    def setUp(self):
        self.date = dateutil.parser.parse("2015-07-05T22:16:18+00:00")
        self.updated_date = dateutil.parser.parse("2020-07-05T22:16:18+00:00")
        self.new_attribute_value = 'new_value'

        self.subject = IdentifiedBase(id=42, created_at=self.date,
                                      updated_at=self.date, attribute='test')

        self.request_params = {self.subject.entity_name(): self.subject._asdict()}
        self.request_params['id'] = str(self.subject.id)
        self.request_params[self.subject.entity_name()]['attribute'] = self.new_attribute_value

        self.successful_response = {'identified_base': {'id': str(self.subject.id),
                                                        'created_at': self.date.isoformat(),
                                                        'updated_at': self.updated_date.isoformat(),
                                                        'attribute': self.new_attribute_value}}

    @not_raises(KalibroClientSaveError)
    def test_successful_save_with_update(self):
        self.subject.request = create_autospec(self.subject.request,
                                               return_value=self.successful_response)
        self.subject.attribute = self.new_attribute_value
        self.subject.save()

        self.subject.request.assert_called_with(action=str(self.subject.id),
                                                params=self.request_params,
                                                method='put',
                                                prefix=self.subject.update_prefix())

        assert_equal(self.subject.id, 42)
        assert_equal(self.subject.created_at,self.date)
        assert_equal(self.subject.updated_at, self.updated_date)
        assert_equal(self.subject.attribute, self.new_attribute_value)

    @not_raises(KalibroClientSaveError)
    def test_successful_update(self):
        self.subject.request = create_autospec(self.subject.request,
                                               return_value=self.successful_response)

        self.subject.update(attribute=self.new_attribute_value)

        self.subject.request.assert_called_with(action=str(self.subject.id),
                                                params=self.request_params,
                                                method='put',
                                                prefix=self.subject.update_prefix())

        assert_equal(self.subject.id, 42)
        assert_equal(self.subject.created_at, self.date)
        assert_equal(self.subject.updated_at, self.updated_date)
        assert_equal(self.subject.attribute, self.new_attribute_value)
