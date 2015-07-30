from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base

@entity_name_decorator
class ModuleResult(attributes_class_constructor('ModuleResultAttr', ()), Base):
    def __init__(self, grade, height, processing_id, parent_id=None, *args, 
                 **kwargs):
        super(ModuleResult, self).__init__(*args, **kwargs)
        self.grade = grade
        self.parent_id = parent_id
        self.height = height
        self.processing_id = processing_id

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        self._grade = float(value)

    @property
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        if value is not None:
            value = int(value)

        self._parent_id = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = int(value)

    @property
    def processing_id(self):
        return self._processing_id

    @processing_id.setter
    def processing_id(self, value):
        self._processing_id = int(value)
