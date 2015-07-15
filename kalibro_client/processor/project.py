from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.processor.base import Base
from kalibro_client.processor.repository import Repository

@entity_name_decorator
class Project(attributes_class_constructor('Project', ('name', 'description')), Base):

    def repositories(self):
        response = self.request('{}/repositories'.format(self.id), method='get')
        return Repository.response_to_objects_array(response)

