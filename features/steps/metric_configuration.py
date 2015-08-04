from behave import *
from nose.tools import assert_true, assert_in, assert_equal, assert_is_instance

from ..tests.factories import MetricConfigurationFactory, \
    LinesOfCodeMetricFactory

from kalibro_client.configurations import MetricConfiguration

from kalibro_client.base import KalibroClientNotFoundError


@when(u'I have a loc configuration within the given kalibro configuration')
def step_impl(context):
    context.metric = LinesOfCodeMetricFactory.build()
    context.metric_configuration = MetricConfigurationFactory.build(
        kalibro_configuration_id=context.kalibro_configuration.id,
        metric=context.metric)
    context.metric_configuration.save()

@then(u'the metric configuration should exist')
def step_impl(context):
    assert_true(MetricConfiguration.exists(context.metric_configuration.id))

@given(u'I have a loc configuration within the given kalibro configuration')
def step_impl(context):
    context.execute_steps(
        u'When I have a loc configuration within the given kalibro configuration')

@when(u'I destroy the metric configuration')
def step_impl(context):
    context.metric_configuration.delete()

@then(u'the metric configuration should no longer exist')
def step_impl(context):
    assert_true(not MetricConfiguration.exists(context.metric_configuration.id))

@when(u'I search a metric configuration with the same id of the given metric configuration')
def step_impl(context):
    context.found_metric_configuration = MetricConfiguration.find(context.metric_configuration.id)

@then(u'it should return the same metric configuration as the given one')
def step_impl(context):
    assert_equal(context.found_metric_configuration, context.metric_configuration)

@when(u'I search an inexistent metric configuration')
def step_impl(context):
    try:
        MetricConfiguration.find(-1)
    except Exception as exception:
        context.response = exception

@given(u'I have a metric configuration within the given kalibro configuration')
def step_impl(context):
    context.metric_configuration = MetricConfigurationFactory.build(
        kalibro_configuration_id=context.kalibro_configuration.id)
    context.metric_configuration.save()

@when(u'I request all metric configurations of the given kalibro configuration')
def step_impl(context):
    context.metric_configurations = MetricConfiguration.metric_configurations_of(
        context.kalibro_configuration.id)

@then(u'I should get a list of its metric configurations')
def step_impl(context):
    assert_in(context.metric_configuration, context.metric_configurations)

@then(u'I should get an empty list of metric configurations')
def step_impl(context):
    assert_equal(len(context.metric_configurations), 0)
