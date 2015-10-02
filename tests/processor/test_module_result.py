from unittest import TestCase
from nose.tools import assert_equal, assert_true, raises
from mock import patch

from kalibro_client.processor import ModuleResult, Processing, Repository

from tests.factories import ModuleResultFactory, KalibroModuleFactory, \
    ProcessingFactory, DateModuleResultFactory, TreeMetricResultFactory, \
    HotspotMetricResultFactory

from tests.helpers import not_raises


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
            kalibro_module_request.assert_called_once_with(action=':id/kalibro_module', params={'id': self.subject.id},
                                                           method='get')

    def test_tree_metric_results(self):
        tree_metric_result = TreeMetricResultFactory.build()
        response = {'tree_metric_results': [tree_metric_result._asdict()]}
        with patch.object(self.subject, 'request',
                          return_value=response) as tree_metric_results_request:
            tree_metric_results = self.subject.tree_metric_results()
            assert_equal(tree_metric_results, [tree_metric_result])
            tree_metric_results_request.assert_called_once_with(
                action=":id/metric_results", params={"id": self.subject.id},
                method="get")

    def test_hotspot_metric_results(self):
        hotspot_metric_result = HotspotMetricResultFactory.build()
        response = {'hotspot_metric_results': [hotspot_metric_result._asdict()]}
        with patch.object(self.subject, 'request', return_value=response) as hotspot_metric_results_request:
            hotspot_metric_results = self.subject.hotspot_metric_results()
            assert_equal(hotspot_metric_results, [hotspot_metric_result])
            hotspot_metric_results_request.assert_called_once_with(
                action=":id/hotspot_metric_results", params={"id": self.subject.id}, method="get")

    def test_descendant_hotspot_metric_results(self):
        hotspot_metric_result = HotspotMetricResultFactory.build()
        response = {'hotspot_metric_results': [hotspot_metric_result._asdict()]}
        with patch.object(self.subject, 'request', return_value=response) as hotspot_metric_results_request:
            hotspot_metric_results = self.subject.descendant_hotspot_metric_results()
            assert_equal(hotspot_metric_results, [hotspot_metric_result])
            hotspot_metric_results_request.assert_called_once_with(
                action=":id/descendant_hotspot_metric_results", params={"id": self.subject.id}, method="get")
