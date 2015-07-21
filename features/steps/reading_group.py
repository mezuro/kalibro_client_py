from behave import *
from nose.tools import assert_true, assert_in, assert_equal

from ..tests.factories import ReadingGroupFactory, ReadingFactory

from kalibro_client.configurations import ReadingGroup

@given(u'I have a reading group with name "{}"')
def step_impl(context, reading_group_name):
    context.reading_group = ReadingGroupFactory.build(name=reading_group_name)
    context.reading_group.save()

@when(u'I ask for all the reading groups')
def step_impl(context):
    context.all_reading_groups = ReadingGroup.all()

@then(u'I should get a list with the given reading group')
def step_impl(context):
    assert_in(context.reading_group, context.all_reading_groups)

@when(u'I create a reading group with name "{}"')
def step_impl(context, reading_group_name):
    context.execute_steps(
        u'Given I have a reading group with name "{}"'.format(reading_group_name))

@then(u'the reading group should exist')
def step_impl(context):
    assert_true(ReadingGroup.exists(context.reading_group.id))

@when(u'I destroy the reading group')
def step_impl(context):
    context.reading_group.delete()

@then(u'the reading group should no longer exist')
def step_impl(context):
    assert_true(not ReadingGroup.exists(context.reading_group.id))
