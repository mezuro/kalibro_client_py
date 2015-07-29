from behave import *
from nose.tools import assert_is_instance

from kalibro_client.errors import KalibroClientNotFoundError

@then(u'I should get an error')
def step_impl(context):
    assert_is_instance(context.response, KalibroClientNotFoundError)
