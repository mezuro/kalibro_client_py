from unittest import TestCase

from mock import patch
from nose.tools import assert_equal, raises

from kalibro_client.configurations.statistic import Statistic


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

    @raises(NotImplementedError)
    def test_not_implemented_find(self):
        Statistic.find(1)

    @raises(NotImplementedError)
    def test_not_implemented_all(self):
        Statistic.all()

    @raises(NotImplementedError)
    def test_not_implemented_exists(self):
        Statistic.exists(1)

    @raises(NotImplementedError)
    def test_not_implemented_save(self):
        self.subject.save()

    @raises(NotImplementedError)
    def test_not_implemented_update(self):
        self.subject.update()

    @raises(NotImplementedError)
    def test_not_implemented_delete(self):
        self.subject.delete()




