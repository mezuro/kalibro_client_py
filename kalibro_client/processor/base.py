import kalibro_client
from kalibro_client.base import IdentityMixin, Base as ClientBase

class Base(IdentityMixin, ClientBase):
    __slots__ = ()

    @classmethod
    def service_address(cls):
        return kalibro_client.config()['kalibro_processor']

class Project(Base):
    def __init__(self, attributes={}):
        self.id = ""
        self.name = ""
        self.description = ""

        super(Project, self).__init__(attributes)