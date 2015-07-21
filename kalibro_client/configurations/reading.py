from kalibro_client.base import attributes_class_constructor, entity_name_decorator
from kalibro_client.configurations.base import Base

@entity_name_decorator
class Reading(attributes_class_constructor('ReadingAttr', ('label', 'grade', 'color')), Base):
    def __init__(self, reading_group_id=None, *init_args, **init_kwargs):
        super(Reading, self).__init__(*init_args, **init_kwargs)
        self.reading_group_id = reading_group_id

    @property
    def reading_group_id(self):
        return self._reading_group_id

    @reading_group_id.setter
    def reading_group_id(self, value):
        if value is not None:
            value = int(value)

        self._reading_group_id = value

    @classmethod
    def readings_of(cls, reading_group_id):
        response = cls.request(action='', params={}, method='get', prefix="reading_groups/{}".format(reading_group_id))
        return Reading.response_to_objects_array(response)

    def save_prefix(self):
        return "reading_groups/{}".format(self.reading_group_id)

    def update_prefix(self):
        return "reading_groups/{}".format(self.reading_group_id)

    def delete_prefix(self):
        return "reading_groups/{}".format(self.reading_group_id)
