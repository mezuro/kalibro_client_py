import requests as req
from collections import namedtuple


class Configuration(namedtuple('Configuration', 'host port')):
    @property
    def service_address(self):
        return "{}:{}".format(self.host, self.port)

    @classmethod
    def from_options(cls, options):
        return cls(**options)


class Base(object):
    def __init__(self, attributes={}):
        for name in attributes:
            try:
                getattr(self, name) # Checks if the attribute is valid
                setattr(self, name, attributes[name])
            except AttributeError:
                pass # Just ignore an invalid attribute

    @classmethod
    def endpoint(cls):
        return cls.entity_name() + "s"

    @classmethod
    def entity_name(cls):
        raise NotImplementedError

    def request(self, action, params, method='post', prefix=''):
        url = "/%s/%s" % (self.endpoint())
        response = getattr(req, method)(url, params=params)
        return response.text

    @staticmethod
    def entity_name_decorator():
        """ Assign an entity name based on the class immediately inhering from Base.

        This is needed because we don't want
        entity names to come from any class that simply inherits our classes, just the ones in our module.

        For example, if you create a class Project2 that exists outside of kalibro_client and inherits from Project,
        it's entity name should still be Project.
        """

        def class_rebuilder(cls):
            class_name = cls.__name__

            class NewClass(cls):
                @classmethod
                def entity_name(cls):
                    return class_name

            return NewClass

        return class_rebuilder
