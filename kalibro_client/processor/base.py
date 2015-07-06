import kalibro_client
from kalibro_client.base import IdentityMixin, Base as ClientBase

class Base(IdentityMixin, ClientBase):
    __slots__ = ()

    @classmethod
    def service_address(cls):
        return kalibro_client.config()['kalibro_processor']
