from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base

@entity_name_decorator
class Processing(attributes_class_constructor('ProcessingAttr',
                                              (('date', None),
                                               ('state', None),
                                               ('error', None),
                                               ('root_module_result_id', None),
                                               ('error_message', None),
                                               ('repository_id', None))),
                 Base):
    pass
