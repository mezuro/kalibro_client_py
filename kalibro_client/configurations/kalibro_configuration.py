from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.configurations.base import Base
from kalibro_client.configurations.metric_configuration import MetricConfiguration

@entity_name_decorator
class KalibroConfiguration(attributes_class_constructor('KalibroConfigurationAttr', ('name', 'description')), Base):

    def metric_configurations(self):
        response = self.request(':id/metric_configurations', {'id':self.id}, method='get')
        return MetricConfiguration.response_to_objects_array(response)