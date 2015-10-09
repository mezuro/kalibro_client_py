from nose.tools import assert_true, assert_equal, raises

from kalibro_client.miscellaneous import Granularity


# This does not subclass TestCase so test generators work
class TestGranularity(object):
    # Note: since we've delegated the implementation of the comparisons to the
    # enum module they won't be tested here

    def test_parent(self):
        def check_parent(child, parent):
            assert_equal(child.parent(), parent)

        # This runs runs the check_parent method with the given parameters as a
        # test. It differs from simply calling assert in that each is an
        # individual test and can fail or succeed on it's own,
        yield check_parent, Granularity.METHOD, Granularity.CLASS
        yield check_parent, Granularity.CLASS, Granularity.PACKAGE
        yield check_parent, Granularity.PACKAGE, Granularity.SOFTWARE
        yield check_parent, Granularity.SOFTWARE, Granularity.SOFTWARE

    def test_str(self):
        assert_equal(str(Granularity.SOFTWARE), 'SOFTWARE')

    def test_comparisons(self):
        def check_equality(granularity1, granularity2):
            assert_true(granularity1 == granularity2)

        yield check_equality, Granularity.SOFTWARE, Granularity.SOFTWARE
        yield check_equality, Granularity.PACKAGE, Granularity.PACKAGE
        yield check_equality, Granularity.CLASS, Granularity.CLASS
        yield check_equality, Granularity.METHOD, Granularity.METHOD
        yield check_equality, Granularity.FUNCTION, Granularity.FUNCTION

        def check_greater_than(granularity1, granularity2):
            assert_true(granularity1 > granularity2)

        yield check_greater_than, Granularity.SOFTWARE, Granularity.PACKAGE
        yield check_greater_than, Granularity.PACKAGE, Granularity.CLASS
        yield check_greater_than, Granularity.CLASS, Granularity.METHOD

        def check_lesser_than(granularity1, granularity2):
            assert_true(granularity1 < granularity2)

        yield check_lesser_than, Granularity.PACKAGE, Granularity.SOFTWARE
        yield check_lesser_than, Granularity.CLASS, Granularity.PACKAGE
        yield check_lesser_than, Granularity.METHOD, Granularity.CLASS
        yield check_lesser_than, Granularity.FUNCTION, Granularity.PACKAGE

    @raises(ValueError)
    def test_invalid_lt_comparisons(self):
        Granularity.METHOD < Granularity.FUNCTION

    @raises(ValueError)
    def test_invalid_eq_comparisons(self):
        Granularity.CLASS == Granularity.FUNCTION

    @raises(ValueError)
    def test_invalid_gt_comparisons(self):
        Granularity.CLASS > Granularity.FUNCTION
