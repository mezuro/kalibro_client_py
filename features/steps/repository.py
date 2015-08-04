from time import sleep

from nose.tools import assert_in

from ..tests.factories import RepositoryFactory
from kalibro_client.processor import Repository

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

@given(u'I have an independent repository')
def step_impl(context):
    context.independent_repository = RepositoryFactory.build()
    context.independent_repository.save()

@when(u'I ask for all the repositories')
def step_impl(context):
    context.repositories = Repository.all()

@then(u'the response should contain the given repositories')
def step_impl(context):
    assert_in(context.repository, context.repositories)
    assert_in(context.independent_repository, context.repositories)
