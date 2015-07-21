import kalibro_client
from kalibro_client.base import BaseCRUD

class Base(BaseCRUD):
    @classmethod
    def service_address(cls):
        return kalibro_client.config()['configurations_address']
