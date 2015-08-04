from behave import *
from nose.tools import assert_is_instance

from kalibro_client.processor import ModuleResult, MetricResult
from kalibro_client.configurations import MetricConfiguration
from kalibro_client.miscellaneous import DateMetricResult

@given(u'I search a metric result with descendant values for the given metric result')
def step_impl(context):
    first_module_result = ModuleResult.find(context.response.root_module_result_id)

    metric_results = first_module_result.metric_results()
    context.response = metric_results[0].descendant_values()

@then(u'I should get a Float list')
def step_impl(context):
    assert_is_instance(context.response, list)
    for element in context.response:
        assert_is_instance(element, float)

@when(u'I call the history of method with the metric name and the results root id of the given processing')
def step_impl(context):
    context.response = MetricResult.history_of(context.metric.name, context.response.root_module_result_id, context.repository.id)

@then(u'I should get a list of date metric results')
def step_impl(context):
    assert_is_instance(context.response, list)
    for element in context.response:
        assert_is_instance(element, DateMetricResult)

@when(u'I call the metric results of method with the results root id of the given processing')
def step_impl(context):
    print(context.response)
    context.response = ModuleResult.find(context.response.root_module_result_id).metric_results()

@then(u'I should get a list of metric results')
def step_impl(context):
    assert_is_instance(context.response, list)
    for element in context.response:
        assert_is_instance(element, MetricResult)

@then(u'the first metric result should have a metric configuration')
def step_impl(context):
    assert_is_instance(context.response[0].metric_configuration(), MetricConfiguration)
