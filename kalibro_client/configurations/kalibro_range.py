from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.configurations.base import Base
from kalibro_client.configurations import MetricConfiguration, Reading

@entity_name_decorator
class KalibroRange(attributes_class_constructor('KalibroRangeAttr', ('beginning', 'end', ('comments', None))), Base):
    def __init__(self, reading_id, metric_configuration_id, *init_args, **init_kwargs):
        super(KalibroRange, self).__init__(*init_args, **init_kwargs)

        self.reading_id = reading_id
        self.metric_configuration_id = metric_configuration_id

        self._reading = None

    @property
    def reading_id(self):
        return self._reading_id

    @reading_id.setter
    def reading_id(self, value):
        self._reading_id = int(value)

    @property
    def metric_configuration_id(self):
        return self._metric_configuration_id

    @metric_configuration_id.setter
    def metric_configuration_id(self, value):
        self._metric_configuration_id = int(value)

    @property
    def reading(self):
        if self._reading is None:
            self._reading = Reading.find(self.reading_id)

        return self._reading

    @property
    def label(self):
        return self.reading.label

    @property
    def grade(self):
        return self.reading.grade

    @property
    def color(self):
        return self.reading.color

    @classmethod
    def ranges_of(cls, metric_configuration_id):
        response = cls.request('', params={'id': metric_configuration_id},
                               method='get', prefix='metric_configurations/:id')
        return cls.response_to_objects_array(response)

    def _asdict(self):
        dict_ = super(KalibroRange, self)._asdict()
        dict_['metric_configuration_id'] = self.metric_configuration_id
        dict_['reading_id'] = self.reading_id
        return dict_

    def save_prefix(self):
        return "metric_configurations/{}".format(self.metric_configuration_id)

    def update_prefix(self):
        return "metric_configurations/{}".format(self.metric_configuration_id)

    def delete_prefix(self):
        return "metric_configurations/{}".format(self.metric_configuration_id)
