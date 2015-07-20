import factory
from kalibro_client.processor import Project, Repository
from kalibro_client.configurations import KalibroConfiguration, MetricConfiguration

class ProjectFactory(factory.Factory):
    class Meta:
        model = Project

    name = 'A random Project'
    description = 'A real example Project'

class RepositoryFactory(factory.Factory):
    class Meta:
        model = Repository

    id = 1
    created_at = None
    updated_at = None
    name = "QtCalculator"
    description = "A simple calculator"
    license = "GPLv3"
    period = 1
    scm_type = "SVN"
    address = "svn://svn.code.sf.net/p/qt-calculator/code/trunk"
    kalibro_configuration_id = 1
    project_id = 1
    code_directory = ""
    branch = "master"

class KalibroConfigurationFactory(factory.Factory):
    class Meta:
        model = KalibroConfiguration

    id = 1
    name = 'Ruby Configuration'
    description = 'A simple Ruby Configuration'

class MetricConfigurationFactory(factory.Factory):
    class Meta:
        model = MetricConfiguration

    id = 1
    created_at = None
    updated_at = None
    metric = None # TODO: Add a Metric instance here
    weight = 1.0
    aggregation_form = "MEAN"
    reading_group_id = 1
    kalibro_configuration_id = 1
