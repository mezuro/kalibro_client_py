from behave import *
from nose.tools import assert_true, assert_in, assert_equal

from ..tests.factories import KalibroConfigurationFactory, \
    MetricConfigurationFactory, ReadingGroupFactory, ReadingFactory, NativeMetricFactory

from kalibro_client.configurations import KalibroConfiguration

@given(u'I have a kalibro configuration with name "{}"')
def step_impl(context, kalibro_configuration_name):
    context.kalibro_configuration = KalibroConfigurationFactory.build(name=kalibro_configuration_name)
    context.kalibro_configuration.save()

@given(u'I have a sample configuration with MetricFu metrics')
def step_impl(context):
  context.reading_group = ReadingGroupFactory.build()
  context.reading_group.save()
  context.reading = ReadingFactory.build(reading_group_id = context.reading_group.id)
  context.reading.save()

  context.kalibro_configuration = KalibroConfigurationFactory.build()
  context.kalibro_configuration.save()

  context.metric = NativeMetricFactory.build()
  metric_configuration = MetricConfigurationFactory.build(metric=context.metric,
                                                          reading_group_id=context.reading_group.id,
                                                          kalibro_configuration_id=context.kalibro_configuration.id)

@when(u'I get all the kalibro configurations')
def step_impl(context):
    context.all_kalibro_configurations = KalibroConfiguration.all()

@then(u'I should get a list with the given kalibro configuration')
def step_impl(context):
    assert_in(context.kalibro_configuration, context.all_kalibro_configurations)

@when(u'I create the kalibro configuration with name "{}"')
def step_impl(context, kalibro_configuration_name):
    context.execute_steps(
        u'Given I have a kalibro configuration with name "{}"'.format(kalibro_configuration_name))

@then(u'the kalibro configuration should exist')
def step_impl(context):
    assert_true(KalibroConfiguration.exists(context.kalibro_configuration.id))

@when(u'I destroy the kalibro configuration')
def step_impl(context):
    context.kalibro_configuration.delete()

@then(u'the kalibro configuration should no longer exist')
def step_impl(context):
    assert_true(not KalibroConfiguration.exists(context.kalibro_configuration.id))

@given(u'the kalibro configuration has a metric configuration')
def step_impl(context):
    context.metric_configuration = MetricConfigurationFactory.build(kalibro_configuration_id=context.kalibro_configuration.id)
    context.metric_configuration.save()

@when(u'I list all the metric configurations of the kalibro configuration')
def step_impl(context):
    context.metric_configurations = context.kalibro_configuration.metric_configurations()

@then(u'I should get a list with the given metric configuration')
def step_impl(context):
    assert_in(context.metric_configuration, context.metric_configurations)
