from behave import *
from nose.tools import assert_true
from ..tests.factories import NativeMetricFactory
from kalibro_client.configurations import Statistic

@given(u'I have a metric with name "Lines of Code"')
def step_impl(context):
    context.loc_metric = NativeMetricFactory.build(name="Lines of Code")

@when(u'I request the metric_percentage')
def step_impl(context):
    context.metric_percentage = Statistic.metric_percentage(
        context.loc_metric.code)

@then(u'I should get a hash containing a real number')
def step_impl(context):
    assert_true(isinstance(context.metric_percentage, dict))
    assert_true(isinstance(context.metric_percentage["metric_percentage"],
                           float))
