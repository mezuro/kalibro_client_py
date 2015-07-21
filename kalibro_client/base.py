from datetime import datetime

import json
import requests
import inflection
import dateutil.parser
import recordtype

from kalibro_client.errors import KalibroClientSaveError, KalibroClientDeleteError, \
    KalibroClientNotFoundError

class RequestMethods(object):
    def save_prefix(self):
        return ""

    def update_prefix(self):
        return ""

    def delete_prefix(self):
        return ""

class Base(object):
    @classmethod
    def _is_valid_field(cls, name):
        return name in cls._fields

    @classmethod
    def response_to_objects_array(cls, response):
        array = response[inflection.pluralize(cls.entity_name())]
        return cls.array_to_objects_array(array)

    @classmethod
    def array_to_objects_array(cls, array):
        return [cls(**attributes) for attributes in array]


class BaseCRUD(Base, RequestMethods):
    @classmethod
    def endpoint(cls):
        return inflection.pluralize(cls.entity_name())

    @classmethod
    def entity_name(cls):
        raise NotImplementedError

    @classmethod
    def service_address(cls):
        raise NotImplementedError

    @classmethod
    def request(cls, action, params=None, method='post', prefix=None):
        url = cls.service_address()

        if prefix:
            url += "/" + prefix
        url += "/{}/{}".format(cls.endpoint(), action)

        if params is not None and 'id' in params:
            url = url.replace(':id', str(params.pop('id')))

        response = requests.request(method, url, data=json.dumps(params),
                                    headers={'Content-Type': 'application/json'})
        return response.json()

    @classmethod
    def find(cls, id):
        response = cls.request(':id', params={'id': id}, method='get')
        if 'errors' in response:
            raise KalibroClientNotFoundError(response['errors'])
        return cls(**response[cls.entity_name()])

    @classmethod
    def all(cls):
        return cls.response_to_objects_array(cls.request('', method='get'))

    @classmethod
    def exists(cls, id):
        return cls.request(':id/exists', params={'id': id}, method='get')['exists']

    def _update_request(self):
        return self.request(action=str(self.id),
                        params={self.entity_name(): self._asdict(), 'id': str(self.id)},
                        method='put',
                        prefix=self.update_prefix())

    def save(self):
        if not self.id:
            response = self.request(action='',
                                    params={self.entity_name(): self._asdict()},
                                    prefix=self.save_prefix())
        else:
            response = self._update_request()

        if 'errors' not in response:
            response_body = response[self.entity_name()]

            self.id = response_body['id']
            self.created_at = response_body['created_at']
            self.updated_at = response_body['updated_at']
        else:
            raise KalibroClientSaveError(response['errors'])

    def update(self, **kwargs):
        if not self.id:
            raise KalibroClientSaveError("Cannot update a record that is not saved.")

        for attr, value in kwargs.items():
            if self._is_valid_field(attr):
                setattr(self, attr, value)

        response = self._update_request()

        if 'errors' in response:
            raise KalibroClientSaveError(response['errors'])

        response_body = response[self.entity_name()]
        self.updated_at = response_body['updated_at']

    def delete(self):
        if not isinstance(self.id, (int, long)):
            raise KalibroClientDeleteError('Can not delete object without id')

        response = self.request(action=':id', params={'id': self.id}, method='delete', prefix=self.delete_prefix())

        if 'errors' in response:
            raise KalibroClientDeleteError(response['errors'])


def entity_name_decorator(top_cls):
    """
    Assign an entity name based on the class immediately inhering from Base.

    This is needed because we don't want
    entity names to come from any class that simply inherits our classes,
    just the ones in our module.

    For example, if you create a class Project2 that exists outside of
    kalibro_client and inherits from Project, it's entity name should still
    be Project.
    """
    class_name = inflection.underscore(top_cls.__name__).lower()

    def entity_name(cls):
        return class_name

    top_cls.entity_name = classmethod(entity_name)

    return top_cls


def attributes_class_constructor(name, fields, identity=True, *args, **kwargs):
    if not identity:
        return recordtype.recordtype(name, fields, *args, **kwargs)

    # Create the new class, inheriting from the record type and from this
    # class
    class IdentityClass(recordtype.recordtype(name, fields, *args, **kwargs)):
        def __init__(self, id=None, created_at=None, updated_at=None,
                     *init_args, **init_kwargs):
            super(IdentityClass, self).__init__(*init_args, **init_kwargs)
            self.id = id
            self.created_at = created_at
            self.updated_at = updated_at

        @property
        def id(self):
            return self._id

        @id.setter
        def id(self, value):
            if value is not None:
                value = int(value)

            self._id = value

        @property
        def created_at(self):
            return self._created_at

        @created_at.setter
        def created_at(self, value):
            if value is not None and not isinstance(value, datetime):
                value = dateutil.parser.parse(value)

            self._created_at = value

        @property
        def updated_at(self):
            return self._updated_at

        @updated_at.setter
        def updated_at(self, value):
            if value is not None and not isinstance(value, datetime):
                value = dateutil.parser.parse(value)

            self._updated_at = value

    return IdentityClass
