from datetime import datetime
import inspect

import requests
import inflection
import dateutil.parser
import recordtype

class Base(object):
    @classmethod
    def endpoint(cls):
        return inflection.pluralize(cls.entity_name())

    @classmethod
    def entity_name(cls):
        raise NotImplementedError

    @classmethod
    def service_address(cls):
        raise NotImplementedError

    def request(self, action, params=None, method='post', prefix=None):
        url = self.service_address()

        if prefix:
            url += "/" + prefix
        else:
            url += ""
        url += "/{}/{}".format(self.endpoint(), action)

        response = requests.request(method, url, params=params)
        return response.json()

    @staticmethod
    def entity_name_decorator():
        """
        Assign an entity name based on the class immediately inhering from Base.

        This is needed because we don't want
        entity names to come from any class that simply inherits our classes,
        just the ones in our module.

        For example, if you create a class Project2 that exists outside of
        kalibro_client and inherits from Project, it's entity name should still
        be Project.
        """

        def class_rebuilder(cls):
            class_name = cls.__name__

            class NewClass(cls):
                @classmethod
                def entity_name(cls):
                    return inflection.underscore(class_name).lower()

            return NewClass

        return class_rebuilder


def attributes_class_constructor(name, fields, identity, *args, **kwargs):
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