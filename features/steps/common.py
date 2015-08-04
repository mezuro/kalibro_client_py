from time import sleep

from behave import *
from nose.tools import assert_is_instance, assert_true

from kalibro_client.errors import KalibroClientNotFoundError

@given(u'I wait up to {} seconds')
def step_impl(context, seconds):
    sleep(int(seconds))

@then(u'I should get an error')
def step_impl(context):
    assert_is_instance(context.response, KalibroClientNotFoundError)

@then(u'I should get true')
def step_impl(context):
    assert_true(context.response)

@then(u'I should get false')
def step_impl(context):
    assert_true(not context.response)
