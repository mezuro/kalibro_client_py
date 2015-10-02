from unittest import TestCase
import dateutil.parser

from nose.tools import assert_true, assert_equal, assert_is_not_none, \
    raises

from tests.factories import DateModuleResultFactory, ModuleResultFactory


class TestDateModuleResult(TestCase):
    def setUp(self):
        self.subject = DateModuleResultFactory.build()
        self.module_result = ModuleResultFactory.build()
        self.second_subject = DateModuleResultFactory.build(date=None, module_result = self.module_result)

    def test_properties_getters(self):
        assert_true(hasattr(self.subject, 'date'))
        assert_true(hasattr(self.subject, 'module_result'))

    @raises(AttributeError)
    def test_properties_setters(self):
        self.subject.date = "2011-10-20T18:27:43.151+00:00"
        self.subject.module_result = self.module_result

    def test_result(self):
        assert_equal(self.subject.result(), self.module_result.grade)

    def test_constructor(self):
        assert_equal(self.subject.date, dateutil.parser.parse(DateModuleResultFactory.date))
        assert_equal(self.second_subject.date, None)
        assert_equal(self.second_subject.module_result, self.module_result)

        assert_is_not_none(self.subject.module_result)
        module_result = self.subject.module_result
        module_result_params = DateModuleResultFactory.module_result

        assert_equal(module_result.grade, float(module_result_params["grade"]))
        assert_equal(module_result.parent_id, module_result_params["parent_id"])
        assert_equal(module_result.processing_id, module_result_params["processing_id"])

    def test_asdict(self):
        dict = self.subject._asdict()

        assert_equal(self.subject.module_result._asdict(), dict["module_result"])

        return dict
