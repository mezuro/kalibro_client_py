import kalibro_client
from kalibro_client.base import Base as ClientBase

class Base(ClientBase):
    @classmethod
    def service_address(cls):
        return kalibro_client.config()['kalibro_processor']
