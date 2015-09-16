from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base
import kalibro_client.configurations.metric_configuration



@entity_name_decorator
class MetricResult(attributes_class_constructor('MetricResultAttrs',
                                                (('module_result_id', None),)),
                   Base):

    def __init__(self, value=None, metric_configuration_id=None,
                 *init_args, **init_kwargs):
        super(MetricResult, self).__init__(*init_args, **init_kwargs)
        self.value = value
        self.metric_configuration_id = metric_configuration_id

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, number):
        if number is not None:
            number = float(number)

        self._value = number

    @property
    def metric_configuration_id(self):
        return self._metric_configuration_id

    @metric_configuration_id.setter
    def metric_configuration_id(self, number):
        if number is not None:
            number = int(number)

        self._metric_configuration_id = number

    def _asdict(self):
        dict_ = super(MetricResult, self)._asdict()

        dict_['value'] = self.value
        dict_['metric_configuration_id'] = self.metric_configuration_id

        return dict_

    def metric_configuration(self):
        return kalibro_client.configurations.metric_configuration.MetricConfiguration.find(self.metric_configuration_id)
