import requests
import inflection

class Base(object):
    def __init__(self, attributes):
        self.attributes = dict(attributes)

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

    def __getattr__(self, attr):
        try:
            return self.attributes[attr]
        except KeyError:
            raise AttributeError('Kalibro Base object has no attribute ' + attr)

    def __setattr__(self, attr, value):
        # Must check if attributes actually exists, or we'll do an infinite loop
        # in the constructor while initializing it.
        if hasattr(self, 'attributes') and attr in self.attributes:
            self.attributes[attr] = value
        else:
            super(Base, self).__setattr__(attr, value)
