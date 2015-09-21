from behave import *
from nose.tools import assert_is_instance, assert_in

from kalibro_client.processor import ModuleResult, MetricResult, TreeMetricResult, HotspotMetricResult
from kalibro_client.configurations import MetricConfiguration
from kalibro_client.miscellaneous import DateMetricResult

@given(u'I search a metric result with descendant values for the given metric result')
def step_impl(context):
    first_module_result = ModuleResult.find(context.response.root_module_result_id)

    metric_results = first_module_result.tree_metric_results()
    context.response = metric_results[0].descendant_values()

@when(u'I call the history of method with the metric name and the results root id of the given processing')
def step_impl(context):
    context.response = TreeMetricResult.history_of(context.metric.name, context.response.root_module_result_id, context.repository.id)

@when(u'I request the first hotspot metric result from the root module result')
def step_impl(context):
    processing = context.repository.last_ready_processing()
    context.hotspot_metric_result = ModuleResult.find(processing.root_module_result_id).hotspot_metric_results()[0]

@when(u'I ask for the related results for the given metric result')
def step_impl(context):
    context.related_results = context.hotspot_metric_result.related_results()

@when(u'I call the metric results of method with the results root id of the given processing')
def step_impl(context):
    context.response = ModuleResult.find(context.response.root_module_result_id).metric_results()

@then(u'I should get a Float list')
def step_impl(context):
    assert_is_instance(context.response, list)
    for element in context.response:
        assert_is_instance(element, float)

@then(u'I should get a list of date metric results')
def step_impl(context):
    assert_is_instance(context.response, list)
    for element in context.response:
        assert_is_instance(element, DateMetricResult)


@then(u'I should get a list of metric results')
def step_impl(context):
    assert_is_instance(context.response, list)
    for element in context.response:
        assert_is_instance(element, MetricResult)

@then(u'the first metric result should have a metric configuration')
def step_impl(context):
    assert_is_instance(context.response[0].metric_configuration(), MetricConfiguration)

@then(u'I should get a list of hotspot metric results including the given one')
def step_impl(context):
    assert_in(context.hotspot_metric_result, context.related_results)
    for hotspot_metric_result in context.related_results:
        assert_is_instance(hotspot_metric_result, HotspotMetricResult)
