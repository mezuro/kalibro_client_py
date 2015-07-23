from behave import *
from nose.tools import assert_true, assert_in, assert_equal

from ..tests.factories import MetricConfigurationFactory

from kalibro_client.configurations import MetricConfiguration


@when(u'I have a loc configuration within the given kalibro configuration')
def step_impl(context):
    context.metric_configuration = MetricConfigurationFactory.build(kalibro_configuration_id=context.kalibro_configuration.id)
    context.metric_configuration.save()

@then(u'the metric configuration should exist')
def step_impl(context):
    assert_true(MetricConfiguration.exists(context.metric_configuration.id))

@given(u'I have a loc configuration within the given kalibro configuration')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I have a loc configuration within the given kalibro configuration')

@when(u'I destroy the metric configuration')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I destroy the metric configuration')

@then(u'the metric configuration should no longer exist')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the metric configuration should no longer exist')

@when(u'I search a metric configuration with the same id of the given metric configuration')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I search a metric configuration with the same id of the given metric configuration')

@then(u'it should return the same metric configuration as the given one')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then it should return the same metric configuration as the given one')

@when(u'I search an inexistent metric configuration')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I search an inexistent metric configuration')

@then(u'I should get an error')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get an error')

@given(u'I have a metric configuration within the given kalibro configuration')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I have a metric configuration within the given kalibro configuration')

@when(u'I request all metric configurations of the given kalibro configuration')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I request all metric configurations of the given kalibro configuration')

@then(u'I should get a list of its metric configurations')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a list of its metric configurations')

@then(u'I should get an empty list of metric configurations')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get an empty list of metric configurations')
