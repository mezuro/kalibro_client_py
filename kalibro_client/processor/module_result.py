from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base
from kalibro_client.processor import KalibroModule, Processing, MetricResult, \
    Repository
import kalibro_client.miscellaneous.date_module_result

@entity_name_decorator
class ModuleResult(attributes_class_constructor('ModuleResultAttr', ()), Base):
    def __init__(self, grade, processing_id, parent_id=None, *args,
                 **kwargs):
        super(ModuleResult, self).__init__(*args, **kwargs)
        self.grade = grade
        self.parent_id = parent_id
        self.processing_id = processing_id
        self._kalibro_module = None
        self._processing = None

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if value is not None:
            value = float(value)

        self._grade = value

    @property
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        if value is not None:
            value = int(value)

        self._parent_id = value

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

    @property
    def kalibro_module(self):
        if self._kalibro_module is None:
            self._kalibro_module = KalibroModule(**self.request(
                                                    action=':id/kalibro_module',
                                                    params={'id': self.id},
                                                    method='get')['kalibro_module'])

        return self._kalibro_module

    @property
    def processing(self):
        if self._processing is None:
            self._processing = Processing.find(self.processing_id)

        return self._processing

    def is_folder(self):
        return len(self.children()) > 0

    def is_file(self):
        return not self.is_folder()

    @classmethod
    def history_of(cls, module_result, repository_id):
        response = Repository.request(action=':id/module_result_history_of',
                                      params={'id': repository_id, 'kalibro_module_id': module_result.kalibro_module.id})['module_result_history_of']
        return [kalibro_client.miscellaneous.date_module_result.DateModuleResult(element[0], element[1]) for element in response]

    def metric_results(self):
        return MetricResult.response_to_objects_array(self.request(
                                                action=':id/metric_results',
                                                params={'id': self.id},
                                                method='get'))
