from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.configurations.base import Base

@entity_name_decorator
class RangeSnapshot(attributes_class_constructor('RangeSnapshotAttr', ('label', 'color', 'comments'), False), Base):
    def __init__(self, beginning=None, end=None, grade=None, *init_args, **init_kwargs):
        super(RangeSnapshot, self).__init__(*init_args, **init_kwargs)
        self.beginning = beginning
        self.end = end
        self.grade = grade

    @property
    def beginning(self):
        return self._beginning

    @beginning.setter
    def beginning(self, value):
        self._beginning = float(value)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = float(value)

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        self._grade = float(value)
