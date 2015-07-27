from kalibro_client.configurations.base import Base
from kalibro_client.base import entity_name_decorator

@entity_name_decorator
class Statistic(Base):
    @classmethod
    def metric_percentage(cls, metric_code):
        return cls.request("/metric_percentage",
            {"metric_code": metric_code}, method="get")

    @classmethod
    def find(cls, id):
        raise NotImplementedError

    @classmethod
    def all(cls):
        raise NotImplementedError

    @classmethod
    def exists(cls, id):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def update(self, **kwargs):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
