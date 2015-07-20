from behave import *
from nose.tools import assert_true, assert_in, assert_equal

from ..tests.factories import ProjectFactory

from kalibro_client.processor import Project

@given(u'I have a project with name "{}"')
def step_impl(context, project_name):
    context.execute_steps(
        u'When I create the project with name "{}"'.format(project_name))

@given(u'I set the project name to "{}"')
def step_impl(context, project_name):
    context.project.name = project_name

@when(u'I create the project with name "{}"')
def step(context, project_name):
    context.project = ProjectFactory.build(name=project_name)
    context.project.save()

@when(u'I search a project with the same id of the given project')
def step_impl(context):
    context.found_project = Project.find(context.project.id)

@when(u'I destroy the project with the same id of the given project')
def step_impl(context):
    context.found_project = Project.find(context.project.id)
    context.found_project.delete()

@when(u'I ask for all the projects')
def step_impl(context):
    context.all_projects = Project.all()

@given(u'I save the given project')
def step_impl(context):
    # The method save does not return so we test that no exceptions are raised
    context.project.save()

@then(u"the project should exist")
def step(context):
    assert_true(Project.exists(context.project.id))

@then(u'it should return the same project as the given one')
def step_impl(context):
    assert_equal(context.project, context.found_project)

@then(u'the project should no longer exist')
def step_impl(context):
    assert_true(not Project.exists(context.found_project.id))

@then(u'I should get a list with the given project')
def step_impl(context):
    assert_in(context.project, context.all_projects)

@then(u'I should get true as the response')
def step_impl(context):
    pass
