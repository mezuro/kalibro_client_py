import factory
from kalibro_client.processor import Project, Repository, Processing,\
    KalibroModule
from kalibro_client.configurations import KalibroConfiguration,\
    MetricConfiguration


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


class ProcessingFactory(factory.Factory):
    class Meta:
        model = Processing

    id = 31
    date = "2011-10-20T18:26:43.151+00:00"
    state = "READY"
    root_module_result_id = 13
    repository_id = 1

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

class KalibroModuleFactory(factory.Factory):
    class Meta:
        model = KalibroModule

    id = 1
    granlrty = None # TODO add a Granularity instance here
    long_name = "kalibro_client_py.tests.factories"
    module_result_id = 1
