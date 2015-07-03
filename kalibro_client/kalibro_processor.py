from kalibro_client.base import Base, Configuration

class KalibroProcessorBase(Base):
    configuration = Configuration('localhost', '8082')

    def __init__(self, attributes={}):
        super(KalibroProcessorBase, self).__init__(attributes)

class Project(KalibroProcessorBase):
    def __init__(self, attributes={}):
        self.id = ""
        self.name = ""
        self.description = ""

        super(Project, self).__init__(attributes)