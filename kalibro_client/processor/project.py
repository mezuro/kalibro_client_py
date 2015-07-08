from kalibro_client.base import attributes_class_constructor
from kalibro_client.processor.base import Base

@Base.entity_name_decorator()
class Project(attributes_class_constructor('Project', ('name', 'description')), Base):
    pass
