from behave import *
from nose.tools import assert_true, assert_in, assert_equal

from ..tests.factories import MetricCollectorDetailsFactory

from kalibro_client.processor import MetricCollectorDetails
from kalibro_client.errors import KalibroClientError

@when(u'I get all metric collector names')
def step_impl(context):
    context.all_names = MetricCollectorDetails.all_names()

@then(u'it should return Analizo string inside of an array')
def step_impl(context):
    assert_in("Analizo", context.all_names)

@when(u'I search metric collector Analizo by name')
def step_impl(context):
    context.analizo_details = MetricCollectorDetails.find_by_name("Analizo")

@then(u'I should get Analizo metric collector')
def step_impl(context):
    assert_equal(context.analizo_details.name, "Analizo")

@when(u'I search metric collector Avalio by name')
def step_impl(context):
    try:
        MetricCollectorDetails.find_by_name("Avalio")
    except KalibroClientError as exception:
        context.response = exception
