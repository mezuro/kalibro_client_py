from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base
from kalibro_client.processor import Repository
import kalibro_client.miscellaneous.date_metric_result



@entity_name_decorator
class MetricResult(attributes_class_constructor('MetricResultAttrs',
                                                (('module_result_id', None),)),
                   Base):

    def __init__(self, value=None, metric_configuration_id=None,
                 aggregated_value=None, *init_args, **init_kwargs):
        super(MetricResult, self).__init__(*init_args, **init_kwargs)
        self.value = float(aggregated_value) if value is None else float(value)
        self.metric_configuration_id = metric_configuration_id
        self.aggregated_value = aggregated_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, number):
        if number is not None:
            number = float(number)

        self._value = number

    @property
    def aggregated_value(self):
        return self._aggregated_value

    @aggregated_value.setter
    def aggregated_value(self, number):
        if number is not None:
            number = float(number)

        self._aggregated_value = number

    @property
    def metric_configuration_id(self):
        return self._metric_configuration_id

    @metric_configuration_id.setter
    def metric_configuration_id(self, number):
        if number is not None:
            number = int(number)

        self._metric_configuration_id = number

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
        return map(lambda a: kalibro_client.miscellaneous.date_metric_result.DateMetricResult(a), response)
