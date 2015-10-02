from kalibro_client.configurations.base import Base
from kalibro_client.base import entity_name_decorator, RequestMethods

@entity_name_decorator
class Statistic(RequestMethods):
    @classmethod
    def metric_percentage(cls, metric_code):
        return cls.request("/metric_percentage",
            {"metric_code": metric_code}, method="get")

    @classmethod
    def service_address(cls):
        return Base.service_address()
