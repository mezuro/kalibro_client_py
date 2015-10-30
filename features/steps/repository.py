from time import sleep
from datetime import datetime, timedelta

from behave import *
from nose.tools import assert_in, assert_is_instance, assert_true, assert_equal

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

@given(u'I have an independent repository')
def step_impl(context):
    context.independent_repository = RepositoryFactory.build()
    context.independent_repository.save()

@given(u'I call the first_processing method for the given repository')
def step_impl(context):
    context.execute_steps(u'when I call the first_processing method for the given repository')

@given(u'I have the given repository')
def step_impl(context):
    row = dict(zip(context.table.headings, context.table[0].cells))
    context.repository = RepositoryFactory.build(
        kalibro_configuration_id=context.kalibro_configuration.id, **row)
    context.repository.save()

@when(u'I call the processing method for the given repository')
def step_impl(context):
    context.response = context.repository.processing()

@when(u'I ask for all the repositories')
def step_impl(context):
    context.repositories = Repository.all()

@when(u'I call the first_processing method for the given repository')
def step_impl(context):
    context.response = context.repository.first_processing()

@when(u'I call the first_processing_after method for the given repository and yesterday\'s date')
def step_impl(context):
    yesterday = datetime.now() - timedelta(hours=24)
    context.response = context.repository.first_processing_after(yesterday)

@when(u'I call the has_processing for the given repository')
def step_impl(context):
    context.response = context.repository.has_processing()

@when(u'I call the has_processing_after for the given repository with yerterday\'s date')
def step_impl(context):
    yesterday = datetime.now() - timedelta(hours=24)
    context.response = context.repository.has_processing_after(yesterday)

@when(u'I call the has_processing_before for the given repository with tomorrows\'s date')
def step_impl(context):
    tomorrow = datetime.now() + timedelta(hours=24)
    context.response = context.repository.has_processing_before(tomorrow)

@when(u'I call the has_ready_processing for the given repository')
def step_impl(context):
    context.response = context.repository.has_ready_processing()

@when(u'I call the last_processing method for the given repository')
def step_impl(context):
    context.response = context.repository.last_processing()

@when(u'I call the last_processing_before method for the given repository and tomorrow\'s date')
def step_impl(context):
    tomorrow = datetime.now() + timedelta(hours=24)
    context.response = context.repository.last_processing_before(tomorrow)

@when(u'I call the last_processing_state method for the given repository')
def step_impl(context):
    context.response = context.repository.last_processing_state()

@when(u'I call the last_ready_processing method for the given repository')
def step_impl(context):
    context.response = context.repository.last_ready_processing()

@when(u'I call the processing_with_date method for the given repository and tomorrow\'s date')
def step_impl(context):
    tomorrow = datetime.now() + timedelta(hours=24)
    context.response = context.repository.processing_with_date(tomorrow)

@when(u'I call the processing_with_date method for the given repository and yesterday\'s date')
def step_impl(context):
    yesterday = datetime.now() - timedelta(hours=24)
    context.response = context.repository.processing_with_date(yesterday)

@when(u'I destroy the repository')
def step_impl(context):
    context.repository.delete()

@when(u'I ask to check if the given repository exists')
def step_impl(context):
    context.response = Repository.exists(context.repository.id)

@when(u'I ask to find the given repository')
def step_impl(context):
    context.found_repository = Repository.find(context.repository.id)

@when(u'I wait up for a ready processing')
def step_impl(context):
    context.execute_steps(u'Given I wait up for a ready processing')

@when(u'I ask for repositories from the given project')
def step_impl(context):
    context.project_repositories = Repository.repositories_of(context.project.id)

@then(u'the response should contain the given repositories')
def step_impl(context):
    assert_in(context.repository, context.repositories)
    assert_in(context.independent_repository, context.repositories)

@then(u'this processing should have process times')
def step_impl(context):
    assert_true(len(context.response.process_times()) > 0)

@then(u'the repository should no longer exist')
def step_impl(context):
    assert_true(not Repository.exists(context.repository.id))

@then(u'I should get the given repository')
def step_impl(context):
    assert_equal(context.repository, context.found_repository)

@then(u'I should get a list with the given repository')
def step_impl(context):
    assert_in(context.repository, context.project_repositories)

@then(u'the repositories should contain the project id')
def step_impl(context):
    assert_equal(context.project_repositories[0].project_id, context.project.id)

@when(u'I call the cancel_process method for the given repository')
def step_impl(context):
    context.response = context.repository.cancel_processing_of_a_repository()

@then(u'I should get success')
def step_impl(context):
    assert_true("errors" not in context.response)

@when(u'I call the process method for the given repository')
def step_impl(context):
    context.response = context.repository.process()

@when(u'I list types')
def step_impl(context):
    context.repository_types = Repository.repository_types()

@then(u'I should get an array of types')
def step_impl(context):
    assert_is_instance(context.repository_types, list)
    assert_true(len(context.repository_types) >= 1)
    assert_in("GIT", context.repository_types)
    assert_in("SVN", context.repository_types)
