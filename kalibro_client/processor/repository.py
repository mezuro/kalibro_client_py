from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.processor.base import Base

@entity_name_decorator
class Repository(attributes_class_constructor('Repository', ('name', 'description', 'license', 'period', 'scm_type', 'address', 'kalibro_configuration_id', 'project_id', 'send_email', 'code_directory', 'branch')), Base):
    pass
