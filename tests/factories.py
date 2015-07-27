import factory

from kalibro_client.miscellaneous import NativeMetric, CompoundMetric, \
    DateModuleResult, DateMetricResult
from kalibro_client.processor import Project, Repository, Processing,\
    KalibroModule, ProcessTime
from kalibro_client.configurations import KalibroConfiguration,\
    MetricConfiguration, ReadingGroup, Reading


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

class ProcessTimeFactory(factory.Factory):
    class Meta:
        model = ProcessTime

    created_at = None
    updated_at = None
    state = "READY"
    processing_id = 1
    time = 1


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

    name = 'Ruby Configuration'
    description = 'A simple Ruby Configuration'

class MetricConfigurationFactory(factory.Factory):
    class Meta:
        model = MetricConfiguration

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

class NativeMetricFactory(factory.Factory):
    class Meta:
        model = NativeMetric

    type = "NativeMetricSnapshot"
    name = "Cyclomatic Complexity"
    code = "saikuro"
    scope = "METHOD"
    description = ""
    languages = ["RUBY"]
    metric_collector_name = "MetricFu"

class CompoundMetricFactory(factory.Factory):
    class Meta:
        model = CompoundMetric

    type = "CompoundMetricSnapshot"
    name = "Lines of Code"
    code = "loc"
    scope = "CLASS"
    description = ""
    script = "return 0;"

class ReadingGroupFactory(factory.Factory):
    class Meta:
        model = ReadingGroup

    name = "Sample reading group"
    description = "Sample reading group"

class ReadingFactory(factory.Factory):
    class Meta:
        model = Reading

    label = "Reading"
    grade = 10
    color = "33dd33"
    reading_group_id = 1

class DateMetricResultFactory(factory.Factory):
    class Meta:
        model = DateMetricResult

    date = "2011-10-20T18:26:43.151+00:00"

    metric_result = {
        'value': "1.0",
        'module_result_id': 1,
        'metric_configuration_id': 1
    }

class DateModuleResultFactory(factory.Factory):
    class Meta:
        model = DateModuleResult

    date = "2011-10-20T18:26:43.151+00:00"
    module_result = None