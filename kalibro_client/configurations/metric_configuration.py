from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.configurations.base import Base

@entity_name_decorator
class MetricConfiguration(attributes_class_constructor('KalibroConfiguration', ('metric', 'weight', 'aggregation_form', 'reading_group_id', 'kalibro_configuration_id')), Base):
    pass