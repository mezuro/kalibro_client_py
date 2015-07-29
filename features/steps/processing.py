from behave import *
from nose.tools import assert_is_instance, assert_equal
from time import sleep

from ..tests.factories import RepositoryFactory

from kalibro_client.processor import ProcessTime

@given(u'the given project has the following Repositories')
def step_impl(context):
    row = dict(zip(context.table.headings, context.table[0].cells))
    context.repository = RepositoryFactory.build(
        project_id=context.project.id, kalibro_configuration_id=context.kalibro_configuration.id, **row)
    context.repository.save()

@given(u'I call the process method for the given repository')
def step_impl(context):
    context.repository.process()

@given(u'I wait up for a ready processing')
def step_impl(context):
    while not context.repository.has_ready_processing():
        sleep(10)

@when(u'I call the processing method for the given repository')
def step_impl(context):
    context.processing = context.repository.processing()

@when(u'I call the processes_times method for the given processing')
def step_impl(context):
    context.process_times = context.processing.process_times()

@then(u'I should get a list of ProcessTimes')
def step_impl(context):
    assert_equal(len(context.process_times), 1)
    for process_time in context.process_times:
        assert_is_instance(process_time, ProcessTime)
