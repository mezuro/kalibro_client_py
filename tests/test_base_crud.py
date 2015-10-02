import dateutil.parser

from unittest import TestCase
from mock import create_autospec, patch
from nose.tools import assert_equal, raises, assert_raises_regexp, assert_true

from .helpers import not_raises

from kalibro_client.errors import KalibroClientSaveError, KalibroClientDeleteError, \
    KalibroClientNotFoundError
from kalibro_client.base import BaseCRUD, attributes_class_constructor, \
    entity_name_decorator


@entity_name_decorator
class IdentifiedBase(attributes_class_constructor('Identified',
                                                  ('attribute')), BaseCRUD):
    pass


class TestBaseCRUD(TestCase):
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

    @raises(KalibroClientSaveError)
    def test_unsuccessful_save(self):
        subject = IdentifiedBase(attribute='test')

        unsuccessful_response = {'errors': ['A string with an error']}
        subject.request = create_autospec(subject.request, return_value=unsuccessful_response)

        subject.save()

        subject.request.assert_called_with('', {subject.entity_name() : subject._asdict()})

    def test_unsuccessful_update_without_id(self):
        subject = IdentifiedBase(id=None, attribute='test')
        subject.request = create_autospec(subject.request,
            side_effect=AssertionError("Request should not be called for update without id"))

        with assert_raises_regexp(KalibroClientSaveError,
                                  "Cannot update a record that is not saved."):
            subject.update(attribute='new value')

    @raises(KalibroClientSaveError)
    def test_unsuccessful_update(self):
        subject = IdentifiedBase(id=42, attribute='test')
        unsuccessful_response = {'errors': ['A string with an error']}

        subject.request = create_autospec(subject.request, return_value=unsuccessful_response)

        subject.update(attribute='new_value')

    def test_all(self):
        hash_array = [{'attribute': 'fizz'},
                      {'attribute': 'zzif'}]
        response = {'derived': hash_array}
        objects = [IdentifiedBase(id=1, attribute='fizz'),
                   IdentifiedBase(id=1, attribute='zzif')]
        with patch.object(IdentifiedBase, 'request', return_value=response) as request_mock, \
             patch.object(IdentifiedBase, 'response_to_objects_array', return_value=objects) as mock:
            IdentifiedBase.all()
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
