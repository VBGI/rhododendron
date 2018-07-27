from django.test import TestCase, TransactionTestCase

from .models import Species, Image, Record


# ------- test constants --------------

# attributes for testing

species_allowed_attributes = ('name', 'info', 'created', 'updated')

record_allowed_attributes = ('species', 'updated', 'created', 'region',
                             'district', 'content', 'latitude', 'longitude')

image_allowed_attributes = ('description', 'title', 'created', 'updated',
                             'src', 'record', 'order')
# -------------------------------------

def auto_attr_helper(model_name, *args):
    '''Autotest class-decorator

    Creates tests and check for attribute existence
    '''

    def wrapped(arg):
        def _check_attr(self):
            self.assertTrue(hasattr(getattr(self, model_name), arg))
        return _check_attr

    class AutoAttrChecker(type):
        def __new__(cls, name, bases, attrs):
            for arg in args:
                attrs['test_{}_{}'.format(model_name, arg)] = wrapped(arg)
            bases = (TestCase, )
            return super().__new__(cls, name, bases, attrs)
    return AutoAttrChecker



# ------------- Test classes -------------

class BasicSpeciesTests(metaclass=auto_attr_helper('species',
                                                 *species_allowed_attributes)):
    @classmethod
    def setUpTestData(cls):
        cls.species = Species.objects.create(name='Test')

    def test_species_name(self):
        self.assertEqual(self.species.name, 'Test')


class BasicImagesTests(metaclass=auto_attr_helper('image',
                                                *image_allowed_attributes)):
    @classmethod
    def setUpTestData(cls):
        cls.image = Image.objects.create()


class BasicRecordTests(metaclass=auto_attr_helper('record',
                                                *record_allowed_attributes)):
    @classmethod
    def setUpTestData(cls):
        cls.species = Species.objects.create(name='Test')
        cls.record = Record.objects.create(species=cls.species)


