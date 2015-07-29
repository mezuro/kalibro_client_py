from behave import *
from nose.tools import assert_true, assert_in, assert_equal

from ..tests.factories import MetricCollectorDetailsFactory

from kalibro_client.processor import MetricCollectorDetails
from kalibro_client.errors import KalibroClientError

@when(u'I get all metric collector names')
def step_impl(context):
    context.all_names = MetricCollectorDetails.all_names()

@then(u'it should return MetricFu string inside of an array')
def step_impl(context):
    assert_in("MetricFu", context.all_names)

@when(u'I search metric collector MetricFu by name')
def step_impl(context):
    context.metric_fu_etails = MetricCollectorDetails.find_by_name("MetricFu")

@then(u'I should get MetricFu metric collector')
def step_impl(context):
    assert_equal(context.metric_fu_etails.name, "MetricFu")

@when(u'I search metric collector Avalio by name')
def step_impl(context):
    try:
        MetricCollectorDetails.find_by_name("Avalio")
    except KalibroClientError as exception:
        context.response = exception
