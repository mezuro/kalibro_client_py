import requests as req

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

class Configuration(object):
    def __init__(self, attributes):
        self.host = ""
        self.port = ""

        self.configure(attributes)

    def service_address(self):
        return "%s:%s" % (self.host, self.port)

    def configure(self, attributes={}):
        for name in attributes:
                try:
                    getattr(self, name) # Checks if the attribute is valid
                    setattr(self, name, attributes[name])
                except AttributeError:
                    pass # Just ignore an invalid attribute
