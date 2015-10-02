from unittest import TestCase

from mock import patch
from nose.tools import assert_equal, assert_true, raises
import dateutil.parser

from kalibro_client.base import attributes_class_constructor, \
    entity_name_decorator, Base

from .helpers import not_raises


class Derived(attributes_class_constructor('DerivedAttr',
                                           ('name', 'description'),
                                           identity=False), Base):
    pass


@entity_name_decorator
class DerivedWithEntityName(attributes_class_constructor('DerivedAttr', ('name', 'description'), identity=False), Base):
    pass


class TestBase(TestCase):
    def setUp(self):
        self.attributes = {'name': 'A random Project',
                           'description': 'A real example Project'}
        self.base = Derived(**self.attributes)

    def test_init(self):
        assert_equal(self.base.name, self.attributes['name'])
        assert_equal(self.base.description, self.attributes['description'])

    def test_is_valid_field(self):
        assert_true(Derived._is_valid_field('name'))
        assert_true(Derived._is_valid_field('description'))
        assert_true(not Derived._is_valid_field('invalid'))
        assert_true(not Derived._is_valid_field('errors'))

    def test_response_to_objects_array(self):
        array = [DerivedWithEntityName('fizz', 'buzz'), DerivedWithEntityName('zzif', 'zzub')]
        with patch.object(DerivedWithEntityName, 'array_to_objects_array', return_value=array) as mock:
            hash_array = [{'name': 'fizz', 'description': 'buzz'},
                          {'name': 'zzif', 'description': 'zzub'}]
            response = {'derived_with_entity_names': hash_array}
            DerivedWithEntityName.response_to_objects_array(response)
            mock.assert_called_once_with(hash_array)

    def test_array_to_objects_array(self):
        array = [{'name': 'fizz', 'description': 'buzz'},
                 {'name': 'zzif', 'description': 'zzub'}]
        assert_equal(DerivedWithEntityName.array_to_objects_array(array),
                     [DerivedWithEntityName('fizz', 'buzz'),
                     DerivedWithEntityName('zzif', 'zzub')])


class TestsEntityNameDecorator(TestCase):
    @entity_name_decorator
    class Entity(Base):
        def __init__(self):
            pass

    class EntitySubclass(Entity):
        pass

    def test_decorator(self):
        entity = self.Entity()
        assert_equal(
            entity.entity_name(), "entity",
            "Deriving classes with the decorator should be automatically named")

    def test_decorator_with_subclass(self):
        entity_sub = self.EntitySubclass()
        assert_equal(
            entity_sub.entity_name(), "entity",
            "Deriving classes without the decorator should keep the name of "
            "their superclass")

    def test_decorator_with_composite_name(self):
        assert_equal(
            DerivedWithEntityName.entity_name(), "derived_with_entity_name",
            "Entity name should be underscored and lowercased")


class TestAttributesClassConstructor(TestCase):
    class Identified(attributes_class_constructor('IdentifiedAttr', ())):
        pass

    def setUp(self):
        self.identified = self.Identified()

    def test_properties_getters(self):
        assert_true(hasattr(self.identified, 'id'))
        assert_true(hasattr(self.identified, 'created_at'))
        assert_true(hasattr(self.identified, 'updated_at'))

    @not_raises((AttributeError, ValueError))
    def test_properties_setters(self):
        self.identified.id = None
        self.identified.created_at = None
        self.identified.updated_at = None

    @not_raises(ValueError)
    def test_id_setter(self):
        self.identified.id = 10
        self.identified.id = "10"

    @raises(ValueError)
    def test_id_setter_invalid(self):
        self.identified.id = "wrong"

    @not_raises(ValueError)
    def test_created_at_setter(self):
        # ISO8601 format
        date_str = "2015-07-05T22:16:18+00:00"
        self.identified.created_at = date_str

        date_obj = dateutil.parser.parse(date_str)
        self.identified.created_at = date_obj

    @raises(ValueError)
    def test_created_at_setter_invalid(self):
        self.identified.created_at = "wrong"

    @not_raises(ValueError)
    def test_updated_at_setter(self):
        # ISO8601 format
        date_str = "2015-07-05T22:16:18+00:00"
        self.identified.updated_at = date_str

        date_obj = dateutil.parser.parse(date_str)
        self.identified.updated_at = date_obj

    @raises(ValueError)
    def test_updated_at_setter_invalid(self):
        self.identified.updated_at = "wrong"
