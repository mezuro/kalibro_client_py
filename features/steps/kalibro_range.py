from behave import *
from nose.tools import assert_true, assert_equal, assert_is_not_none, assert_is_none, assert_in

from kalibro_client.configurations import Reading, KalibroRange
from ..tests.factories import AnotherKalibroRangeFactory, KalibroRangeFactory

@given(u'I have a range within the given reading')
def step_impl(context):
    context.range = KalibroRangeFactory.build(reading_id=context.reading.id,
                                              metric_configuration_id=context.metric_configuration.id,
                                              beginning=1.1, end=5.1)
    context.range.save()

@given(u'I have an unsaved range within the given reading')
def step_impl(context):
    context.range = KalibroRangeFactory.build(reading_id=context.reading.id,
                                              metric_configuration_id=context.metric_configuration.id)

@given(u'I have another range within the given reading')
def step_impl(context):
    context.another_range = AnotherKalibroRangeFactory.build(reading_id=context.reading.id,
                                                             metric_configuration_id=context.metric_configuration.id)
    context.another_range.save()

@when(u'I destroy the range')
def step_impl(context):
    context.range.delete()

@when(u'I search a range with the same id of the given range')
def step_impl(context):
    context.found_range = KalibroRange.find(int(context.range.id))

@when(u'I ask ranges of the given metric configuration')
def step_impl(context):
    context.response = KalibroRange.ranges_of(context.metric_configuration.id)

@when(u'I ask to save the given range')
def step_impl(context):
    context.range.save()

@then(u'the range should no longer exist')
def step_impl(context):
    assert_true(not KalibroRange.exists(context.range.id))

@then(u'the range should exist')
def step_impl(context):
    assert_true(KalibroRange.exists(context.range.id))

@then(u'it should return the same range as the given one')
def step_impl(context):
    assert_equal(context.found_range, context.range)

@then(u'I should get an empty list')
def step_impl(context):
    assert_equal(len(context.response), 0)

@then(u'I should get a list with the given range')
def step_impl(context):
    assert_equal(len(context.response), 1)
    assert_equal(context.response[0], context.range)

@then(u'the id of the given range should be set')
def step_impl(context):
    assert_is_not_none(context.range.id)

@when(u'I change the "{}" to "{}"')
def step_impl(context, attribute, value):
    setattr(context.range, attribute, value)

@when(u'I ask to update the given range')
def step_impl(context):
    try:
        context.range.update()
    except Exception as e:
        context.error = e
    else:
        context.error = None

@then(u'I should not receive errors')
def step_impl(context):
    assert_is_none(context.error)

@then(u'I should get the error "{}"')
def step_impl(context, message):
    assert_in(message, context.error.args[0])

