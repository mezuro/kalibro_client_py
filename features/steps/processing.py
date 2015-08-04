from behave import *
from nose.tools import assert_is_instance, assert_true

from kalibro_client.processor import ProcessTime

@when(u'I call the processes_times method for the given processing')
def step_impl(context):
    context.process_times = context.processing.process_times()

@then(u'I should get a list of ProcessTimes')
def step_impl(context):
    assert_true(len(context.process_times) > 0)
    for process_time in context.process_times:
        assert_is_instance(process_time, ProcessTime)
