from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base


@entity_name_decorator
class ProcessTime(attributes_class_constructor('ProcessTimeAttr',
                                               ('state',
                                               ('processing_id', None))),
                  Base):
    def __init__(self, time=None, *init_args, **init_kwargs):
        super(ProcessTime, self).__init__(*init_args, **init_kwargs)
        self.time = time

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if value is not None:
            value = int(value)

        self._time = value
