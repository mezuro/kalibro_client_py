from time import sleep

from behave import *
from nose.tools import assert_in, assert_is_instance

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

@when(u'I call the processing method for the given repository')
def step_impl(context):
    context.processing = context.repository.processing()

@when(u'I ask for all the repositories')
def step_impl(context):
    context.repositories = Repository.all()

@when(u'I call the first_processing method for the given repository')
def step_impl(context):
    context.response = context.repository.first_processing()

@then(u'the response should contain the given repositories')
def step_impl(context):
    assert_in(context.repository, context.repositories)
    assert_in(context.independent_repository, context.repositories)

@when(u'I call the cancel_process method for the given repository')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the cancel_process method for the given repository')

@then(u'I should get success')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get success')

@when(u'I destroy the repository')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I destroy the repository')

@then(u'the repository should no longer exist')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the repository should no longer exist')

@when(u'I ask to check if the given repository exists')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I ask to check if the given repository exists')

@when(u'I ask to find the given repository')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I ask to find the given repository')

@then(u'I should get the given repository')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get the given repository')

@when(u'I ask for repositories from the given project')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I ask for repositories from the given project')

@then(u'I should get a list with the given repository')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a list with the given repository')

@then(u'the repositories should contain the project id')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the repositories should contain the project id')

@when(u'I call the process method for the given repository')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the process method for the given repository')

@when(u'I list types')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I list types')

@then(u'I should get an array of types')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get an array of types')

@when(u'I call the first_processing_after method for the given repository and yesterday\'s date')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the first_processing_after method for the given repository and yesterday\'s date')

@when(u'I call the has_processing for the given repository')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the has_processing for the given repository')

@when(u'I call the has_processing_after for the given repository with yerterday\'s date')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the has_processing_after for the given repository with yerterday\'s date')

@when(u'I call the has_processing_before for the given repository with tomorrows\'s date')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the has_processing_before for the given repository with tomorrows\'s date')

@when(u'I call the has_ready_processing for the given repository')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the has_ready_processing for the given repository')

@then(u'I should get false')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get false')

@when(u'I call the last_processing method for the given repository')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the last_processing method for the given repository')

@when(u'I call the last_processing_before method for the given repository and tomorrow\'s date')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the last_processing_before method for the given repository and tomorrow\'s date')

@when(u'I call the last_processing_state method for the given repository')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the last_processing_state method for the given repository')

@then(u'I should get "PREPARING"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get "PREPARING"')

@when(u'I call the last_ready_processing method for the given repository')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the last_ready_processing method for the given repository')

@then(u'this processing should have process times')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then this processing should have process times')

@then(u'I should get a Processing with state "PREPARING"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a Processing with state "PREPARING"')

@then(u'I should get a Processing with state "READY"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a Processing with state "READY"')

@when(u'I call the processing_with_date method for the given repository and tomorrow\'s date')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the processing_with_date method for the given repository and tomorrow\'s date')

@when(u'I call the processing_with_date method for the given repository and yesterday\'s date')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I call the processing_with_date method for the given repository and yesterday\'s date')
