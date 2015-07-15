from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.processor.base import Base

@entity_name_decorator
class Repository(attributes_class_constructor('RepositoryAttr', (('name', None), ('description', None), ('license', None), ('scm_type', None), ('address', None), ('code_directory', None), ('branch', None))), Base):
    def __init__(self, period=None, project_id=None, kalibro_configuration_id=None, *init_args, **init_kwargs):
        print(super(Repository, self))
        super(Repository, self).__init__(*init_args, **init_kwargs)
        self.period = period
        self.project_id = project_id
        self.kalibro_configuration_id = kalibro_configuration_id

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        if value is not None:
            value = int(value)

        self._period = value

    @property
    def project_id(self):
        return self._project_id

    @project_id.setter
    def project_id(self, value):
        if value is not None:
            value = int(value)

        self._project_id = value

    @property
    def kalibro_configuration_id(self):
        return self._kalibro_configuration_id

    @kalibro_configuration_id.setter
    def kalibro_configuration_id(self, value):
        if value is not None:
            value = int(value)

        self._kalibro_configuration_id = value

    def process(self):
        return self.request(action = '/process', params = {'id': self.id}, method='get')