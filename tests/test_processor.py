from unittest import TestCase, skip
import dateutil
from nose.tools import assert_equal, assert_true, raises
from mock import patch

import kalibro_client
from kalibro_client.processor import Project, Repository, ProcessTime,\
    MetricCollectorDetails, MetricResult, Processing, ModuleResult
from kalibro_client.configurations import MetricConfiguration
from kalibro_client.processor.base import Base
from kalibro_client.errors import KalibroClientNotFoundError

from factories import ProjectFactory, RepositoryFactory, KalibroModuleFactory,\
    ProcessingFactory, MetricCollectorDetailsFactory, NativeMetricFactory,\
    ProcessTimeFactory, MetricResultFactory, DateMetricResultFactory,\
    ModuleResultFactory, DateModuleResultFactory, MetricConfigurationFactory

from .helpers import not_raises


class TestProcessorBase(TestCase):
    @patch('kalibro_client.config')
    def test_service_address(self, kalibro_client_config):
        kalibro_client_config.return_value = kalibro_client.DEFAULT_CONFIG

        assert_equal(Base.service_address(), kalibro_client.DEFAULT_CONFIG['processor_address'])
        kalibro_client_config.assert_called_once()


class TestProject(TestCase):
    def setUp(self):
        self.project = ProjectFactory.build()
        self.project.id = 1
        self.repository = RepositoryFactory.build()
        self.repositories = [self.repository]

    def test_repositories(self):
        repositories_hash = {"repositories": [self.repository._asdict()]}
        with patch.object(Project, 'request', return_value=repositories_hash) as request_mock, \
        patch.object(Repository, 'response_to_objects_array', return_value=self.repositories) as mock:
            self.project.repositories()
            request_mock.assert_called_once_with("1/repositories", method='get')
            mock.assert_called_once_with(repositories_hash)

class TestProcessTime(TestCase):
    def setUp(self):
        self.subject = ProcessTimeFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'time'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.time = "1"

    def test_time_setter_conversion_to_integer(self):
        self.subject.time = "42"
        assert_equal(self.subject.time, 42)


class TestProcessing(TestCase):
    def setUp(self):
        self.subject = ProcessingFactory.build()
        self.process_time = ProcessTimeFactory.build()
        self.process_times = [self.process_time]

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'date'))
        assert_true(hasattr(self.subject, 'repository_id'))
        assert_true(hasattr(self.subject, 'root_module_result_id'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.date = "1"
        self.subject.repository_id = 1
        self.subject.root_module_result_id = 1

    def test_process_times(self):
        process_times_hash = {"process_times": [self.process_time._asdict()]}
        with patch.object(self.subject, 'request', return_value=process_times_hash) as request_mock, \
        patch.object(ProcessTime, 'response_to_objects_array', return_value=self.process_times) as mock:
            response = self.subject.process_times()
            second_response = self.subject.process_times()
            request_mock.assert_called_once_with(action=':id/process_times', params={'id': self.subject.id}, method='get')
            mock.assert_called_once_with(process_times_hash)
            assert_equal(response, self.process_times)
            assert_equal(response, second_response)

    def test_asdict(self):
        dict_ = self.subject._asdict()

        assert_equal(dict_['repository_id'], self.subject.repository_id)
        assert_equal(dict_['date'], self.subject.date)
        assert_equal(dict_['root_module_result_id'], self.subject.root_module_result_id)


class TestKalibroModule(TestCase):
    def setUp(self):
        self.subject = KalibroModuleFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'name'))

        long_name = "test.name"
        self.subject.long_name = long_name
        assert_equal(self.subject.name, long_name.split("."))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        long_name = "test.name"
        self.subject.name = long_name
        assert_equal(self.subject.long_name, long_name)

        name = ["test", "name"]
        self.subject.name = name
        assert_equal(self.subject.long_name, ".".join(name))

    def test_short_name(self):
        name = ["test", "name"]
        self.subject.name = name
        assert_equal(self.subject.short_name, name[-1])

    def test_granularity(self):
        assert_equal(self.subject.granularity, self.subject.granlrty)


class TestRepository(TestCase):
    def setUp(self):
        self.subject = RepositoryFactory.build()
        self.date_str = "2015-07-05T22:16:18+00:00"
        self.date = dateutil.parser.parse(self.date_str)

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'period'))
        assert_true(hasattr(self.subject, 'project_id'))
        assert_true(hasattr(self.subject, 'kalibro_configuration_id'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.period = None
        self.subject.project_id = None
        self.subject.kalibro_configuration_id = None

    def test_asdict(self):
        dict_ = self.subject._asdict()

        assert_equal(dict_['period'], self.subject.period)
        assert_equal(dict_['project_id'], self.subject.project_id)
        assert_equal(dict_['kalibro_configuration_id'], self.subject.kalibro_configuration_id)

    def test_repository_types(self):
        response = {"types": ["GIT", "SVN"]}
        with patch.object(Repository, 'request', return_value=response) as repository_request:
            assert_equal(self.subject.repository_types(), response["types"])
            repository_request.assert_called_once_with(action='/types', params={}, method='get')

    def test_repository_types_with_none(self):
        response = {"types": None}
        with patch.object(Repository, 'request', return_value=response) as repository_request:
            assert_equal(self.subject.repository_types(), [])
            repository_request.assert_called_once_with(action='/types', params={}, method='get')

    def test_repositories_of(self):
        response = {"repositories": [self.subject._asdict()]}
        with patch.object(Repository, 'request', return_value=response) as request_mock, \
            patch.object(Repository, 'response_to_objects_array', return_value=[self.subject]) as response_to_array_mock:
            repositories = Repository.repositories_of(self.subject.project_id)
            request_mock.assert_called_once_with(
                action='',
                params={'id': self.subject.project_id},
                method='get',
                prefix='projects/:id')
            response_to_array_mock.assert_called_once_with(response)
            assert_equal(repositories, [self.subject])

    def test_process(self):
        with patch.object(Repository, 'request') as repository_request:
            self.subject.process()
            repository_request.assert_called_once_with(action=':id/process', params={'id': self.subject.id}, method='get')

    def test_cancel_processing(self):
        with patch.object(Repository, 'request') as repository_request:
            self.subject.cancel_processing_of_a_repository()
            repository_request.assert_called_once_with(action=':id/cancel_process', params={'id': self.subject.id}, method='get')

    def test_processing_with_ready_processing(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_ready_processing', return_value=True) as has_ready_processing_request, \
             patch.object(Repository, 'last_ready_processing', return_value=processing) as last_ready_processing_request:
            self.subject.processing()
            has_ready_processing_request.assert_called_once()
            last_ready_processing_request.assert_called_once()

    def test_processing_without_ready_processing(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_ready_processing', return_value=False) as has_ready_processing_request, \
             patch.object(Repository, 'last_processing', return_value=processing) as last_processing_request:
            self.subject.processing()
            has_ready_processing_request.assert_called_once()
            last_processing_request.assert_called_once()

    def test_processing_with_date_as_string_after(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=True) as has_processing_after_request, \
             patch.object(Repository, 'first_processing_after', return_value=processing) as first_processing_after_request:
            self.subject.processing_with_date(self.date_str)
            has_processing_after_request.assert_called_once_with(self.date)
            first_processing_after_request.assert_called_once_with(self.date)

    def test_processing_with_date_as_string_before(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=False) as has_processing_after_request, \
             patch.object(Repository, 'has_processing_before', return_value=True) as has_processing_before_request, \
             patch.object(Repository, 'last_processing_before', return_value=processing) as last_processing_before_request:
            self.subject.processing_with_date(self.date_str)
            has_processing_after_request.assert_called_once_with(self.date)
            has_processing_before_request.assert_called_once_with(self.date)
            last_processing_before_request.assert_called_once_with(self.date)

    def test_processing_with_date_as_string(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=False) as has_processing_after_request, \
             patch.object(Repository, 'has_processing_before', return_value=False) as has_processing_before_request:
            assert_equal(self.subject.processing_with_date(self.date_str), None)
            has_processing_after_request.assert_called_once_with(self.date)
            has_processing_before_request.assert_called_once_with(self.date)


    def test_processing_with_date_after(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=True) as has_processing_after_request, \
             patch.object(Repository, 'first_processing_after', return_value=processing) as first_processing_after_request:
            self.subject.processing_with_date(self.date)
            has_processing_after_request.assert_called_once_with(self.date)
            first_processing_after_request.assert_called_once_with(self.date)

    def test_processing_with_date_before(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=False) as has_processing_after_request, \
             patch.object(Repository, 'has_processing_before', return_value=True) as has_processing_before_request, \
             patch.object(Repository, 'last_processing_before', return_value=processing) as last_processing_before_request:
            self.subject.processing_with_date(self.date)
            has_processing_after_request.assert_called_once_with(self.date)
            has_processing_before_request.assert_called_once_with(self.date)
            last_processing_before_request.assert_called_once_with(self.date)

    def test_processing_with_date(self):
        processing = ProcessingFactory.build()
        with patch.object(Repository, 'has_processing_after', return_value=False) as has_processing_after_request, \
             patch.object(Repository, 'has_processing_before', return_value=False) as has_processing_before_request:
            assert_equal(self.subject.processing_with_date(self.date), None)
            has_processing_after_request.assert_called_once_with(self.date)
            has_processing_before_request.assert_called_once_with(self.date)

    def test_has_processing(self):
        has_processing_hash = {'has_processing': True}
        with patch.object(Repository, 'request',
                          return_value=has_processing_hash) as repository_request:
            response = self.subject.has_processing()
            repository_request.assert_called_once_with(':id/has_processing', params={'id': self.subject.id}, method='get')
            assert_equal(response, True)

    def test_has_ready_processing(self):
        has_ready_processing_hash = {'has_ready_processing': True}
        with patch.object(Repository, 'request',
                          return_value=has_ready_processing_hash) as repository_request:
            response = self.subject.has_ready_processing()
            repository_request.assert_called_once_with(':id/has_ready_processing', params={'id': self.subject.id}, method='get')
            assert_equal(response, True)

    def test_has_processing_after(self):
        has_processing_after = {'has_processing_in_time': True}
        with patch.object(Repository, 'request',
                          return_value=has_processing_after) as repository_request:
            response = self.subject.has_processing_after(self.date)
            repository_request.assert_called_once_with(':id/has_processing/after', params={'id': self.subject.id, 'date': self.date_str})
            assert_equal(response, True)

    def test_has_processing_before(self):
        has_processing_before = {'has_processing_in_time': True}
        with patch.object(Repository, 'request',
                          return_value=has_processing_before) as repository_request:
            response = self.subject.has_processing_before(self.date)
            repository_request.assert_called_once_with(':id/has_processing/before', params={'id': self.subject.id, 'date': self.date_str})
            assert_equal(response, True)

    def test_last_processing_state(self):
        processing_state_hash = {'processing_state': 'READY'}
        with patch.object(Repository, 'request',
                          return_value=processing_state_hash) as repository_request:
            response = self.subject.last_processing_state()
            repository_request.assert_called_once_with(':id/last_processing_state', params={'id': self.subject.id}, method='get')
            assert_equal(response, 'READY')

    def test_last_ready_processing(self):
        processing = ProcessingFactory.build()
        processing_hash = {'last_ready_processing': processing._asdict()}
        with patch.object(Repository, 'request',
                          return_value=processing_hash) as repository_request:
            response = self.subject.last_ready_processing()
            repository_request.assert_called_once_with(':id/last_ready_processing', params={'id': self.subject.id}, method='get')
            assert_equal(response, processing)

    def test_first_processing(self):
        processing = ProcessingFactory.build()
        processing_hash = {'processing': processing._asdict()}

        with patch.object(Repository, 'request',
                          return_value=processing_hash) as repository_request:
            response = self.subject.first_processing()
            repository_request.assert_called_once_with(':id/first_processing', params={'id': self.subject.id})
            assert_equal(response, processing)

    def test_last_processing(self):
        processing = ProcessingFactory.build()
        processing_hash = {'processing': processing._asdict()}

        with patch.object(Repository, 'request',
                          return_value=processing_hash) as repository_request:
            response = self.subject.last_processing()
            repository_request.assert_called_once_with(':id/last_processing', params={'id': self.subject.id})
            assert_equal(response, processing)

    def test_first_processing_after(self):
        processing = ProcessingFactory.build()
        processing_hash = {'processing': processing._asdict()}

        with patch.object(Repository, 'request',
                          return_value=processing_hash) as repository_request:
            response = self.subject.first_processing_after(self.date)
            repository_request.assert_called_once_with(':id/first_processing/after', params={'id': self.subject.id, 'date': self.date_str})
            assert_equal(response, processing)

    def test_last_processing_before(self):
        processing = ProcessingFactory.build()
        processing_hash = {'processing': processing._asdict()}

        with patch.object(Repository, 'request',
                          return_value=processing_hash) as repository_request:
            response = self.subject.last_processing_before(self.date)
            repository_request.assert_called_once_with(':id/last_processing/before', params={'id': self.subject.id, 'date': self.date_str})
            assert_equal(response, processing)

    def test_branches(self):
        branches = {'branches': ['master', 'stable']}
        url = 'https://github.com/mezuro/kalibro_client_py.git'
        scm_type = 'GIT'

        with patch.object(Repository, 'request',
                          return_value=branches) as repository_request:
            Repository.branches(url, scm_type)
            repository_request.assert_called_once_with("/branches", {'url': url, 'scm_type': scm_type})

class TestMetricCollectorDetails(TestCase):
    def setUp(self):
        self.subject = MetricCollectorDetailsFactory.build()
        self.native_metric = NativeMetricFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'supported_metrics'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.supported_metrics = None

    def test_supported_metrics_conversion_from_hash(self):
        supported_metrics_hash = {self.native_metric.code: self.native_metric._asdict()}

        self.subject.supported_metrics = supported_metrics_hash

        assert_equal(self.subject.supported_metrics, {self.native_metric.code: self.native_metric})

    def test_find_metric_by_name(self):
        name = self.native_metric.name

        assert_equal(self.subject.find_metric_by_name(name), self.native_metric)

    def test_asdict(self):
        dict = self.subject._asdict()

        assert_equal(self.subject.name, dict["name"])
        assert_equal(self.subject.description, dict["description"])
        assert_equal(self.subject.supported_metrics, dict["supported_metrics"])

    def test_find_by_name(self):
        with patch.object(MetricCollectorDetails, 'request',
                          return_value={'metric_collector_details': self.subject._asdict()}) as metric_collector_details_request:
            assert_equal(MetricCollectorDetails.find_by_name(self.subject.name), self.subject)

            metric_collector_details_request.assert_called_once_with('find', params={"name": self.subject.name})

    @raises(KalibroClientNotFoundError)
    def test_find_by_name_invalid_collector(self):
        error_response = {'error': "Metric Collector '{}' not found.".format(self.subject.name)}
        with patch.object(MetricCollectorDetails, 'request',
                          return_value=error_response) as metric_collector_details_request:
            MetricCollectorDetails.find_by_name(self.subject.name)

    def test_all_names(self):
        names = ['Analizo', 'MetricFu']
        with patch.object(MetricCollectorDetails, 'request',
                          return_value={'metric_collector_names': names}) as metric_collector_details_request:
            all_names = MetricCollectorDetails.all_names()
            assert_equal(all_names, names)
            metric_collector_details_request.assert_called_once_with('names', method='get')

    def test_all(self):
        with patch.object(MetricCollectorDetails, 'request',
                          return_value=[self.subject._asdict()]) as metric_collector_details_request:
            all_metric_collectors = MetricCollectorDetails.all()
            assert_equal(all_metric_collectors, [self.subject])
            metric_collector_details_request.assert_called_once_with('', method='get')


class TestMetricResult(TestCase):
    def setUp(self):
        self.subject = MetricResultFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'value'))
        assert_true(hasattr(self.subject, 'aggregated_value'))
        assert_true(hasattr(self.subject, 'metric_configuration_id'))
        assert_true(hasattr(self.subject, 'module_result_id'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.value = 3
        self.subject.aggregated_value = 3
        self.subject.metric_configuration_id = 4
        self.subject.module_result_id = 4

    def test_value_setter_with_none(self):
        self.subject.value = None

        assert_equal(self.subject.value, None)

    def test_value_setter_with_string(self):
        self.subject.value = "1.1"

        assert_equal(self.subject.value, 1.1)

    def test_aggregated_value_setter_with_none(self):
        self.subject.aggregated_value = None

        assert_equal(self.subject.aggregated_value, None)

    def test_aggregated_value_setter_with_string(self):
        self.subject.aggregated_value = "1.1"

        assert_equal(self.subject.aggregated_value, 1.1)

    def test_metric_configuration_id_setter_with_none(self):
        self.subject.metric_configuration_id = None

        assert_equal(self.subject.metric_configuration_id, None)

    def test_metric_configuration_id_setter_with_string(self):
        self.subject.metric_configuration_id = "42"

        assert_equal(self.subject.metric_configuration_id, 42)

    def test_asdict(self):
        dict = self.subject._asdict()

        assert_equal(self.subject.value, dict["value"])
        assert_equal(self.subject.metric_configuration_id, dict["metric_configuration_id"])
        assert_equal(self.subject.aggregated_value, dict["aggregated_value"])

    def test_descendant_values(self):
        descendant_values_hash = {'descendant_values': ["1.1", "2.2", "3.3"]}
        descendant_values = [1.1, 2.2, 3.3]

        with patch.object(self.subject, 'request', return_value=descendant_values_hash) as request_mock:
            assert_equal(self.subject.descendant_values(), descendant_values)
            request_mock.assert_called_once_with(action=':id/descendant_values', params={'id': self.subject.id}, method='get')

    def test_history_of(self):
        date_metric_result = DateMetricResultFactory.build()
        kalibro_module = KalibroModuleFactory.build(id = 2)
        native_metric = NativeMetricFactory.build()
        repository = RepositoryFactory.build(id = 3)

        metric_result_history_of_hash = {'metric_result_history_of': [date_metric_result._asdict()]}
        with patch.object(Repository, 'request', return_value=metric_result_history_of_hash) as request_mock:
            assert_equal(MetricResult.history_of(native_metric.name, kalibro_module.id,
                                                 repository.id),
                         [date_metric_result])
            request_mock.assert_called_once_with(action=':id/metric_result_history_of',
                                                 params={'metric_name': native_metric.name,
                                                         'kalibro_module_id': kalibro_module.id,
                                                         'id': repository.id})

    def test_metric_configuration(self):
        metric_configuration = MetricConfigurationFactory.build()
        with patch.object(MetricConfiguration, 'find', return_value=metric_configuration) as find_mock:
            assert_equal(self.subject.metric_configuration(), metric_configuration)
            find_mock.assert_called_once_with(self.subject.metric_configuration_id)

class TestModuleResult(TestCase):
    def setUp(self):
        self.subject = ModuleResultFactory.build()

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'grade'))
        assert_true(hasattr(self.subject, 'parent_id'))
        assert_true(hasattr(self.subject, 'processing_id'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.subject.parent_id = None
        self.subject.grade = None

    @raises(TypeError)
    def test_properties_setters_with_invalid_parameters(self):
        self.subject.grade = None
        self.subject.processing_id = None

    def test_asdict(self):
        dict = self.subject._asdict()

        assert_equal(self.subject.grade, dict["grade"])
        assert_equal(self.subject.parent_id, dict["parent_id"])
        assert_equal(self.subject.processing_id, dict["processing_id"])

    def test_children(self):
        child = ModuleResultFactory.build()
        response = {'module_results': [child._asdict()]}
        with patch.object(self.subject, 'request',
                          return_value=response) as module_result_request:
            children = self.subject.children()
            assert_equal(children, [child])
            module_result_request.assert_called_once_with(action=':id/children', params={'id': self.subject.id}, method='get')

    def test_parents(self):
        parent = ModuleResultFactory.build(parent_id=None)
        with patch.object(self.subject, 'find',
                          return_value=parent) as find_request:
            parents = self.subject.parents()
            assert_equal(parents, [parent])
            find_request.assert_called_once_with(self.subject.parent_id)

    def test_kalibro_module(self):
        kalibro_module = KalibroModuleFactory.build()
        response = {'kalibro_module': kalibro_module._asdict()}
        with patch.object(self.subject, 'request',
                          return_value=response) as kalibro_module_request:
            first_kalibro_module = self.subject.kalibro_module
            second_kalibro_module = self.subject.kalibro_module
            assert_equal(first_kalibro_module, kalibro_module)
            assert_equal(first_kalibro_module, second_kalibro_module)
            kalibro_module_request.assert_called_once_with(action=':id/kalibro_module', params={'id': self.subject.id}, method='get')

    def test_processing(self):
        processing = ProcessingFactory.build()
        with patch.object(Processing, 'find',
                          return_value=processing) as find_request:
            first_processing = self.subject.processing
            second_processing = self.subject.processing
            assert_equal(first_processing, processing)
            assert_equal(first_processing, second_processing)
            find_request.assert_called_once_with(self.subject.processing_id)

    def test_is_folder(self):
        response = [ModuleResultFactory.build()]
        with patch.object(self.subject, 'children',
                          return_value=response) as children_request:
            assert_true(self.subject.is_folder())
            children_request.assert_called_once()

    def test_is_folder_with_no_children(self):
        response = []
        with patch.object(self.subject, 'children',
                          return_value=response) as children_request:
            assert_true(not self.subject.is_folder())
            children_request.assert_called_once()

    def test_is_file(self):
        with patch.object(self.subject, 'is_folder',
                          return_value=True) as is_folder_request:
            assert_true(not self.subject.is_file())
            is_folder_request.assert_called_once()

    def test_history_of(self):
        date_module_result = DateModuleResultFactory.build()
        kalibro_module = KalibroModuleFactory.build()
        response_kalibro_module = {'kalibro_module': kalibro_module._asdict()}
        repository_id = 1
        response = {'module_result_history_of': [[date_module_result.date, self.subject._asdict()]]}
        with patch.object(Repository, 'request',
                          return_value=response) as module_result_history_request, \
             patch.object(ModuleResult, 'request', return_value=response_kalibro_module) as kalibro_module_request:
            history_module_results = ModuleResult.history_of(
                                                    module_result=self.subject,
                                                    repository_id=repository_id)
            assert_equal([date_module_result], history_module_results)
            module_result_history_request.assert_called_once_with(
                                            action=':id/module_result_history_of',
                                            params={'id': repository_id,
                                                    'kalibro_module_id': self.subject.kalibro_module.id})
            kalibro_module_request.assert_called_once_with(action=':id/kalibro_module', params={'id': self.subject.id}, method='get')

    def test_metric_result(self):
        metric_result = MetricResultFactory.build()
        response = {'metric_results': [metric_result._asdict()]}
        with patch.object(self.subject, 'request',
                          return_value=response) as metric_results_request:
            metric_results = self.subject.metric_results()
            assert_equal(metric_results, [metric_result])
            metric_results_request.assert_called_once_with(
                action=":id/metric_results", params={"id": self.subject.id},
                method="get")
