import kalibro_client
from kalibro_client.configurations.base import Base

from unittest import TestCase

from mock import patch
from nose.tools import assert_equal


class TestConfigurationsBase(TestCase):
    @patch('kalibro_client.config')
    def test_service_address(self, kalibro_client_config):
        kalibro_client_config.return_value = kalibro_client.DEFAULT_CONFIG

        assert_equal(Base.service_address(), kalibro_client.DEFAULT_CONFIG['configurations_address'])
        kalibro_client_config.assert_called_once()

