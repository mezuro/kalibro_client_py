from nose.tools import assert_is_instance

from kalibro_client.processor import ModuleResult, KalibroModule
from kalibro_client.errors import KalibroClientError

@when(u'I ask for the children of the processing root module result')
def step_impl(context):
    context.children = ModuleResult.find(context.repository.processing().root_module_result_id).children()

@then(u'I should get a list with the children module results')
def step_impl(context):
    assert_is_instance(context.children, list)
    for element in context.children:
        assert_is_instance(element, ModuleResult)

@then(u'The first children should have a module')
def step_impl(context):
    assert_is_instance(context.children[0].kalibro_module, KalibroModule)

@when(u'I get the module result of the processing')
def step_impl(context):
    context.module_result = ModuleResult.find(context.repository.processing().root_module_result_id)

@then(u'I should get a module_result')
def step_impl(context):
    assert_is_instance(context.module_result, ModuleResult)

@when(u'I ask for an inexistent module result')
def step_impl(context):
    try:
        ModuleResult.find(-1)
    except KalibroClientError as exception:
        context.response = exception

@given(u'I get the module result of the processing')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I get the module result of the processing')

@when(u'I ask for the history of the given module result')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I ask for the history of the given module result')

@then(u'I should get a list with date module results')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a list with date module results')
