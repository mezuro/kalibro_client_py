from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.configurations.base import Base

@entity_name_decorator
class Reading(attributes_class_constructor('ReadingAttr', ('label', 'grade', 'color', 'reading_group_id')), Base):
    pass
