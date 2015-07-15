from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.processor.base import Base

@entity_name_decorator
class Repository(attributes_class_constructor('Repository', (('name', None), ('description', None), ('license', None), ('period', None), ('scm_type', None), ('address', None), ('kalibro_configuration_id', None), ('project_id', None), ('code_directory', None), ('branch', None))), Base):
    pass
