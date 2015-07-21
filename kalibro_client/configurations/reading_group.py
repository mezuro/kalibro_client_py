from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.configurations.base import Base
from kalibro_client.configurations.reading import Reading

@entity_name_decorator
class ReadingGroup(attributes_class_constructor('ReadingGroupAttr', ('name', ('description', None))), Base):

    def readings(self):
        response = self.request(':id/readings', {'id':self.id}, method='get')
        return Reading.response_to_objects_array(response)
