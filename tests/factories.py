import factory

from kalibro_client.miscellaneous import NativeMetric, CompoundMetric, \
    DateModuleResult, DateMetricResult
from kalibro_client.processor import Project, Repository, Processing,\
    KalibroModule, ProcessTime, MetricCollectorDetails, MetricResult,\
    ModuleResult
from kalibro_client.configurations import KalibroConfiguration,\
    MetricConfiguration, ReadingGroup, Reading, RangeSnapshot, \
    KalibroRange


class ProjectFactory(factory.Factory):
    class Meta:
        model = Project

    name = 'A random Project'
    description = 'A real example Project'


class RepositoryFactory(factory.Factory):
    class Meta:
        model = Repository

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
    code_directory = None
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


class LinesOfCodeMetricFactory(factory.Factory):
    class Meta:
        model = NativeMetric

    type = "NativeMetricSnapshot"
    name = "Lines of Code"
    code = "loc"
    scope = "CLASS"
    description = ""
    languages = ["C"]
    metric_collector_name = "Analizo"


class MetricConfigurationFactory(factory.Factory):
    class Meta:
        model = MetricConfiguration

    created_at = None
    updated_at = None
    metric = NativeMetricFactory.build()
    weight = 1.0
    aggregation_form = "MEAN"
    reading_group_id = 1
    kalibro_configuration_id = 1


class KalibroModuleFactory(factory.Factory):
    class Meta:
        model = KalibroModule

    id = 1
    granlrty = None  # TODO add a Granularity instance here
    long_name = "kalibro_client_py.tests.factories"
    module_result_id = 1


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


class KalibroRangeFactory(factory.Factory):
    class Meta:
        model = KalibroRange

    beginning = 1.1
    end = 5.1
    reading_id = 3
    comments = "Comment"
    metric_configuration_id = 1


class AnotherKalibroRangeFactory(KalibroRangeFactory):
    beginning = 0.0
    end = 1.1
    comments = "Another Comment"

class ModuleResultFactory(factory.Factory):
    class Meta:
        model = ModuleResult

    grade = 10.0
    parent_id = 21
    processing_id = 1

class DateModuleResultFactory(factory.Factory):
    class Meta:
        model = DateModuleResult

    date = "2011-10-20T18:26:43.151+00:00"
    module_result = ModuleResultFactory.build()._asdict()


class RangeSnapshotFactory(factory.Factory):
    class Meta:
        model = RangeSnapshot

    beginning = 1.1
    end = 5.1
    label = "Snapshot"
    grade = 10.1
    color = "FF2284"
    comments = "Comment"

class MetricCollectorDetailsFactory(factory.Factory):
    class Meta:
        model = MetricCollectorDetails

    name = "MetricFu"
    description = ""
    supported_metrics = {NativeMetricFactory.build().code: NativeMetricFactory.build()}

class MetricResultFactory(factory.Factory):
    class Meta:
        model = MetricResult

    metric_configuration_id = 1
    value = 10
    aggregated_value = 5
