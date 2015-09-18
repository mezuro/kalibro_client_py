from kalibro_client.base import entity_name_decorator
from kalibro_client.processor import MetricResult
from kalibro_client.processor import Repository
import kalibro_client.miscellaneous.date_metric_result

@entity_name_decorator
class HotspotMetricResult(MetricResult):
    def __init__(self, line_number=None, message=None,  *init_args, **init_kwargs):
        super(HotspotMetricResult, self).__init__(*init_args, **init_kwargs)
        self.line_number = line_number
        self.message = message

    @property
    def line_number(self):
        return self._line_number

    @line_number.setter
    def line_number(self, number):
        if number is not None:
            number = int(number)

        self._line_number = number

    def related_results(self):
        related_results = self.request(action=':id/related_results', params={'id': self.id}, method='get')
        return HotspotMetricResult.response_to_objects_array(related_results)

    def _asdict(self):
        dict_ = super(HotspotMetricResult, self)._asdict()

        dict_['line_number'] = self.line_number
        dict_['message'] = self.message

        return dict_
