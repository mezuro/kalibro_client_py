from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base


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
