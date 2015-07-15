from behave import *
from nose.tools import assert_is_not_none

from kalibro_client.processor import Project


@when('I create the project with name "{}"')
def step(context, project_name):
    context.project = Project(name=project_name, description="Test project")
    context.project.save()


@then("the project should exist")
def step(context):
    assert_is_not_none(context.project.id)
