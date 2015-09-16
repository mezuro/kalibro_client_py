from kalibro_client.processor import MetricResult
from kalibro_client.processor import Repository
import kalibro_client.miscellaneous.date_metric_result


class TreeMetricResult(MetricResult):

    def __init__(self, aggregated_value=None, *init_args, **init_kwargs):
        super(TreeMetricResult, self).__init__(*init_args, **init_kwargs)
        self.aggregated_value = aggregated_value

    @property
    def aggregated_value(self):
        return self._aggregated_value

    @aggregated_value.setter
    def aggregated_value(self, number):
        if number is not None:
            number = float(number)

        self._aggregated_value = number

    def descendant_values(self):
        descendant_values = self.request(action=':id/descendant_values',
                                         params={'id': self.id},
                                         method='get')['descendant_values']
        return map(float, descendant_values)

    @classmethod
    def history_of(cls, metric_name, kalibro_module_id, repository_id):
        response = Repository.request(action=':id/metric_result_history_of',
                                      params={'metric_name': metric_name,
                                              'kalibro_module_id': kalibro_module_id,
                                              'id': repository_id})['metric_result_history_of']
        return [kalibro_client.miscellaneous.date_metric_result.DateMetricResult(**date_metric_result_hash) for date_metric_result_hash in response]

    def _asdict(self):
        dict_ = super(TreeMetricResult, self)._asdict()

        dict_['aggregated_value'] = self.aggregated_value

        return dict_

    @classmethod
    def endpoint(self):
        return super(TreeMetricResult, self).endpoint()
