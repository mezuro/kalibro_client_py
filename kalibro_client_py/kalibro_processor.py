from kalibro_client_py.base import Base

class KalibroProcessorBase(Base):
    self.host = 'localhost'
    self.port = '8082'

    def __init__(self, attributes={}):

        super(KalibroProcessorBase, self).__init__(attributes)

class Project(KalibroProcessorBase):
    def __init__(self, attributes={}):
        self.id = ""
        self.name = ""
        self.description = ""

        print self.__endpoint

        super(Project, self).__init__(attributes)