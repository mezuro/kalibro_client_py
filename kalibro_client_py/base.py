import requests as req
from collections import namedtuple


class Base(object):
    configuration = Configuration(None, None)

    def __init__(self, attributes={}):
        for name in attributes:
                try:
                    getattr(self, name) # Checks if the attribute is valid
                    setattr(self, name, attributes[name])
                except AttributeError:
                    pass # Just ignore an invalid attribute

    def request(action, params, method='post', prefix=''):
        url = "/%s/%s" % (endpoint)
        response = getattr(req, method)(url, params=params)
        response.text

        
class Configuration(namedtuple('Configuration', 'host port')):
    @property
    def service_address(self):
        return "{}:{}".format(self.host, self.port)

    @classmethod
    def from_options(cls, options):
        return cls(**options)