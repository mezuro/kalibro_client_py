from kalibro_client_py.base import Configuration
from nose.tools import assert_equal

class TestConfiguration(object):
    def setUp(self):
        self.host = 'localhost'
        self.port = '8000'
        self.configuration = Configuration(self.host, self.port)

    def test_init(self):
        assert_equal(self.configuration.host, self.host)
        assert_equal(self.configuration.port, self.port)

    def test_service_address(self):
        assert_equal(self.configuration.service_address,
                     "{}:{}".format(self.host, self.port))

    def test_from_options(self):
        # This kind of assert works just because configuration is a namedtuple
        assert_equal(Configuration.from_options({'host': self.host,
                                                 'port': self.port}),
                     self.configuration)
