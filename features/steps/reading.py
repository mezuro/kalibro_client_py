from behave import *

from nose.tools import assert_true, assert_in, assert_equal

from ..tests.factories import ReadingFactory

from kalibro_client.configurations import Reading


@given(u'the given reading group has the following readings')
def step_impl(context):
    print(context.table[0].cells)
    row = dict(zip(context.table.headings, context.table[0].cells))
    context.reading = ReadingFactory.build(
        reading_group_id=context.reading_group.id, **row)
    print(context.reading)
    context.reading.save()

@when(u'I destroy the reading')
def step_impl(context):
    context.reading.delete()

@then(u'the reading should no longer exist')
def step_impl(context):
    assert_true(not Reading.exists(context.reading.id))

@when(u'I ask to check if the given reading exists')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I ask to check if the given reading exists')

@then(u'I should get true')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get true')

@given(u'I have a reading within the given reading group')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I have a reading within the given reading group')

@when(u'I ask for a reading with the same id of the given reading')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I ask for a reading with the same id of the given reading')

@then(u'I should get the given reading')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get the given reading')

@when(u'I ask for the readings of the given reading group')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I ask for the readings of the given reading group')

@then(u'I should get a list with the given reading')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a list with the given reading')
