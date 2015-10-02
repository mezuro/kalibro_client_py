from unittest import TestCase

from mock import patch
from nose.tools import assert_equal, raises

from kalibro_client.configurations.statistic import Statistic
from kalibro_client.configurations.base import Base


class TestStatistic(TestCase):
    def setUp(self):
        self.subject = Statistic()

    def test_metric_percentage(self):
        response = {"metric_percentage": 10.0}

        with patch.object(Statistic, 'request', return_value=response) as request_mock:
            result = Statistic.metric_percentage('test_metric')
            request_mock.assert_called_once_with('/metric_percentage',
                {'metric_code': 'test_metric'}, method='get')

            assert_equal(result, response)

    def test_service_address(self):
        with patch.object(Base, 'service_address', return_value="address") as service_address_mock:
            Statistic.service_address()
            service_address_mock.assert_called()
