from kalibro_client.base import attributes_class_constructor,\
    entity_name_decorator
from kalibro_client.configurations.base import Base
from kalibro_client.miscellaneous import CompoundMetric, Metric, NativeMetric


@entity_name_decorator
class MetricConfiguration(attributes_class_constructor('MetricConfigurationAttr', ('aggregation_form')), Base):
    def __init__(self, metric, reading_group_id=None, kalibro_configuration_id=None, weight=None, *init_args, **init_kwargs):
        super(MetricConfiguration, self).__init__(*init_args, **init_kwargs)
        self.reading_group_id = reading_group_id
        self.kalibro_configuration_id = kalibro_configuration_id
        self.weight = weight
        self.metric = metric

    @property
    def reading_group_id(self):
        return self._reading_group_id

    @reading_group_id.setter
    def reading_group_id(self, value):
        if value is not None:
            value = int(value)

        self._reading_group_id = value

    @property
    def kalibro_configuration_id(self):
        return self._kalibro_configuration_id

    @kalibro_configuration_id.setter
    def kalibro_configuration_id(self, value):
        if value is not None:
            value = int(value)

        self._kalibro_configuration_id = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if value is not None:
            value = float(value)
        self._weight = value

    def _asdict(self):
        dict_ = super(MetricConfiguration, self)._asdict()
        dict_['metric'] = self.metric._asdict()
        dict_['kalibro_configuration_id'] = self.kalibro_configuration_id
        dict_['reading_group_id'] = self.reading_group_id
        dict_['weight'] = self.weight
        return dict_

    @property
    def metric(self):
        return self._metric

    @metric.setter
    def metric(self, value):
        if isinstance(value, dict):
            if value['type'] == "NativeMetricSnapshot":
                self._metric = NativeMetric(**value)
            else:
                self._metric = CompoundMetric(**value)
        elif isinstance(value, Metric):
            self._metric = value
        else:
            raise ValueError("Cannot cast {} into Metric".format(value))

    @classmethod
    def metric_configurations_of(cls, kalibro_configuration_id):
        return cls.response_to_objects_array(
            cls.request('',
                        {'id': kalibro_configuration_id},
                        method='get',
                        prefix='kalibro_configurations/:id'))
