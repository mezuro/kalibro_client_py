from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base

from datetime import datetime
import dateutil

@entity_name_decorator
class Processing(attributes_class_constructor('ProcessingAttr',
                                              (('state', None),
                                               ('error', None),
                                               ('error_message', None))),
                 Base):

    def __init__(self, repository_id, date, root_module_result_id,
                 *init_args, **init_kwargs):
        super(Processing, self).__init__(*init_args, **init_kwargs)
        self.repository_id = repository_id
        self.date = date
        self.root_module_result_id = root_module_result_id

    @property
    def repository_id(self):
        return self._repository_id

    @repository_id.setter
    def repository_id(self, value):
        if value is not None:
            value = int(value)

        self._repository_id = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, datetime):
            value = dateutil.parser.parse(value)

        self._date = value

    @property
    def root_module_result_id(self):
        return self._root_module_result_id

    @root_module_result_id.setter
    def root_module_result_id(self, value):
        if value is not None:
            value = int(value)

        self._root_module_result_id = value

    def _asdict(self):
        dict_ = super(Processing, self)._asdict()
        dict_["repository_id"] = self.repository_id
        dict_["date"] = self.date
        dict_["root_module_result_id"] = self.root_module_result_id
        return dict_
