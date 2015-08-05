from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator
from kalibro_client.processor.base import Base
from kalibro_client.processor import Processing

import dateutil


@entity_name_decorator
class Repository(attributes_class_constructor('RepositoryAttr',
                                              (('name', None),
                                               ('description', None),
                                               ('license', None),
                                               ('scm_type', None),
                                               ('address', None),
                                               ('code_directory', None),
                                               ('branch', None))), Base):
    def __init__(self, period=None, project_id=None,
                 kalibro_configuration_id=None, *init_args, **init_kwargs):
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

    def _asdict(self):
        dict_ = super(Repository, self)._asdict()

        dict_['period'] = self.period
        dict_['project_id'] = self.project_id
        dict_['kalibro_configuration_id'] = self.kalibro_configuration_id

        return dict_

    @classmethod
    def repository_types(cls):
        response = cls.request(action='/types', params={}, method='get')['types']
        if response == None: response = []
        return response

    @classmethod
    def repositories_of(cls, project_id):
        return cls.response_to_objects_array(cls.request(action='',
            params={'id': project_id},
            method='get',
            prefix="projects/:id"))

    def process(self):
        return self.request(action=':id/process', params={'id': self.id},
                            method='get')

    def cancel_processing_of_a_repository(self):
        return self.request(action=':id/cancel_process',
                            params={'id': self.id},
                            method='get')

    def processing(self):
        if self.has_ready_processing():
            return self.last_ready_processing()
        return self.last_processing()

    def processing_with_date(self, date):
        date = dateutil.parser.parse(date) \
            if isinstance(date, (str, unicode)) else date
        if self.has_processing_after(date):
            return self.first_processing_after(date)
        elif self.has_processing_before(date):
            return self.last_processing_before(date)
        else:
            return None

    def has_processing(self):
        return self.request(':id/has_processing',
                            params={'id': self.id},
                            method='get')['has_processing']

    def has_ready_processing(self):
        return self.request(":id/has_ready_processing",
                            params={'id': self.id},
                            method='get')['has_ready_processing']

    def has_processing_after(self, date):
        return self.request(":id/has_processing/after",
                            params={'id': self.id,
                                    'date': date.isoformat()})['has_processing_in_time']

    def has_processing_before(self, date):
        return self.request(":id/has_processing/before",
                            params={'id': self.id,
                                    'date': date.isoformat()})['has_processing_in_time']

    def last_processing_state(self):
        return self.request(":id/last_processing_state",
                            params={'id': self.id},
                            method='get')['processing_state']

    def last_ready_processing(self):
        return Processing(**self.request(
            ':id/last_ready_processing',
            params={'id': self.id}, method='get')['last_ready_processing'])

    def first_processing(self):
        return Processing(**self.request(":id/first_processing",
                                         params={'id': self.id})['processing'])

    def last_processing(self):
        return Processing(**self.request(":id/last_processing",
                                         params={'id': self.id})['processing'])

    def first_processing_after(self, date):
        return Processing(**self.request(":id/first_processing/after",
                                         params={'id': self.id,
                                                 'date': date.isoformat()})["processing"])

    def last_processing_before(self, date):
        return Processing(**self.request(":id/last_processing/before",
                                         params={'id': self.id,
                                                 'date': date.isoformat()})['processing'])

    @classmethod
    def branches(cls, url, scm_type):
        return cls.request("/branches", {'url': url, 'scm_type': scm_type})
