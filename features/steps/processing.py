from behave import *
from nose.tools import assert_is_instance, assert_true, assert_equal, assert_in

from kalibro_client.processor import Processing, ProcessTime

@when(u'I call the processes_times method for the given processing')
def step_impl(context):
    context.process_times = context.processing.process_times()

@then(u'I should get a list of ProcessTimes')
def step_impl(context):
    assert_true(len(context.process_times) > 0)
    for process_time in context.process_times:
        assert_is_instance(process_time, ProcessTime)

@then(u'I should get a Processing')
def step_impl(context):
    assert_is_instance(context.response, Processing)

@then(u'I should get a Processing with state "{}"')
def step_impl(context, state):
    assert_equal(context.response.state, state)

@then(u'I should get a valid state')
def step_impl(context):
    states = ["PREPARING", "DOWNLOADING", "COLLECTING",
            "CHECKING", "BUILDING", "AGGREGATING", "CALCULATING", "INTERPRETING"]
    assert_in(context.response, states)
