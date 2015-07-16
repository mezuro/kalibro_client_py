from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.configurations.base import Base

@entity_name_decorator
class MetricConfiguration(attributes_class_constructor('MetricConfigurationAttr', ('metric', 'weight', 'aggregation_form')), Base):
    def __init__(self, reading_group_id=None, kalibro_configuration_id=None, *init_args, **init_kwargs):
        super(MetricConfiguration, self).__init__(*init_args, **init_kwargs)
        self.reading_group_id = reading_group_id
        self.kalibro_configuration_id = kalibro_configuration_id

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
