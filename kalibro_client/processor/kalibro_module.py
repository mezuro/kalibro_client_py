from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base

@entity_name_decorator
class KalibroModule(attributes_class_constructor('KalibroModuleAttr',
                                               (('granlrty', None),
                                               ('long_name', None),
                                               ('module_result_id', None))),
                    Base):

    @property
    def name(self):
        return self.long_name.split(".")

    @name.setter
    def name(self, value):
        self.long_name = ".".join(value) if isinstance(value, list) else value

    @property
    def short_name(self):
        return self.name[-1]

    @property
    def granularity(self):
        return self.granlrty
