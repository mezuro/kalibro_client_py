from behave import *
from nose.tools import assert_true, assert_in, assert_equal
from ..tests.factories import NativeMetricFactory, MetricConfigurationFactory

@given(u'I have a metric with name "Lines of Code"')
def step_impl(context):
    context.loc_metric = NativeMetricFactory.build(name="Lines of Code")

@given(u'I have a loc configuration within the given kalibro configuration')
def step_impl(context):
    context.metric_configuration = MetricConfigurationFactory(
        metric=context.loc_metric,
        kalibro_configuration_id=context.kalibro_configuration.id)
    context.metric_configuration.save()

@when(u'I request the metric_percentage')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I request the metric_percentage')

@then(u'I should get a hash containing a real number')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a hash containing a real number')
