from kalibro_client.processor.base import Base

@Base.entity_name_decorator()
class Project(Base.recordtype('Project', ('name', 'description'))):
    pass