from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base
from kalibro_client.processor import KalibroModule, Processing

@entity_name_decorator
class ModuleResult(attributes_class_constructor('ModuleResultAttr', ()), Base):
    def __init__(self, grade, height, processing_id, parent_id=None, *args,
                 **kwargs):
        super(ModuleResult, self).__init__(*args, **kwargs)
        self.grade = grade
        self.parent_id = parent_id
        self.height = height
        self.processing_id = processing_id
        self._kalibro_module = None
        self._processing = None

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

    def _asdict(self):
        dict_ = super(ModuleResult, self)._asdict()
        dict_['grade'] = self.grade
        dict_['parent_id'] = self.parent_id
        dict_['height'] = self.height
        dict_['processing_id'] = self.processing_id
        return dict_

    def children(self):
        return self.response_to_objects_array(self.request(
                                                action=':id/children',
                                                params={'id': self.id},
                                                method='get'))

    def parents(self):
        if self.parent_id is None:
            return []

        parent = self.find(self.parent_id)
        parent_list = parent.parents()
        parent_list.append(parent)
        return parent_list

    def kalibro_module(self):
        if self._kalibro_module is None:
            self._kalibro_module = KalibroModule(**self.request(
                                                    action=':id/kalibro_module',
                                                    params={'id': self.id},
                                                    method='get')['kalibro_module'])

        return self._kalibro_module

    def processing(self):
        if self._processing is None:
            self._processing = Processing.find(self.processing_id)

        return self._processing

    def is_folder(self):
        return len(self.children()) > 0

    def is_file(self):
        return not self.is_folder()
