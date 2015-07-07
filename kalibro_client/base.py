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

    @classmethod
    def all_fields(cls):
        visited = set()
        result = []
        for base in inspect.getmro(cls):
            fields = getattr(base, 'fields', None)
            if not fields or fields in visited:
                continue

            visited.add(fields)
            result.extend(fields)

        return result

    @classmethod
    def recordtype(cls, name, fields, *args, **kwargs):
        all_fields = list(cls.all_fields())
        all_fields.extend(fields)
        # Place fields with defaults last
        all_fields.sort(key=lambda v: isinstance(v, tuple))

        # Don't disable slots unless explicitly requested
        kwargs.setdefault('use_slots', False)

        # Create the new class, inheriting from the record type and from this
        # class
        class NewClass(cls, recordtype.recordtype(name, all_fields, *args,
                                                  **kwargs)):
            pass

        NewClass.__name__ = name
        NewClass.fields = fields
        return NewClass


class IdentityMixin(object):
    fields = (('id', None), ('created_at', None), ('updated_at', None))

    @property
    def id(self):
        return super(IdentityMixin, self).id

    @id.setter
    def id(self, value):
        value = int(value)
        super(IdentityMixin, self).id = value

    @property
    def created_at(self):
        return super(IdentityMixin, self).created_at

    @created_at.setter
    def created_at(self, value):
        if not isinstance(value, datetime):
            value = dateutil.parser.parse(value)

        super(IdentityMixin, self).created_at = value

    @property
    def updated_at(self):
        return super(IdentityMixin, self).updated_at

    @updated_at.setter
    def updated_at(self, value):
        if value is not None and not isinstance(value, datetime):
            value = dateutil.parser.parse(value)

        super(IdentityMixin, self).updated_at = value
