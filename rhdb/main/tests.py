from django.test import TestCase, TransactionTestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Species, Image, Record
from .filters import RecordFilter
from django.urls import reverse


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


# ----------- Filtering engine testing ------------

class ListRecordsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        sp1 = Species.objects.create(name='Test')
        sp2 = Species.objects.create(name='West')
        Record.objects.create(species=sp1, district='Home')
        Record.objects.create(species=sp1, district='Gnome')
        Record.objects.create(species=sp2, district='Valley')
        Record.objects.create(species=sp2, district='Home')
        cls.clien = Client()

    def test_record_filter_basic(self):
        filter = RecordFilter({'district__icontains': 'me'})
        self.assertEqual(filter.qs.count(), 3)

    def test_record_filter_related(self):
        filter = RecordFilter({'species__name__icontains': 'Te'})
        self.assertEqual(filter.qs.count(), 2)

    def test_record_filter_region(self):
        filter = RecordFilter({'region__icontains': 'bob'})
        self.assertEqual(filter.qs.count(), 0)

    def test_record_filter_complex(self):
        filter = RecordFilter({'species__name__icontains': 'est',
                               'district__icontains': 'me'})
        self.assertEqual(filter.qs.count(), 3)

    def test_record_filter_all(self):
        filter = RecordFilter({})
        self.assertEqual(filter.qs.count(), 4)

    def test_request_status(self):
        response = self.client.get(reverse('record-list'), {})
        self.assertEqual(response.status_code, 200)

    def test_request_base_filter(self):
        response = self.client.get(reverse('record-list'),
                                   {'species__name__icontains': 'Te'})
        self.assertContains(response, 'Test')
        self.assertNotContains(response, 'West')

    def test_request_complex_filter(self):
        response = self.client.get(reverse('record-list'),
                                   {'species__name__icontains': 'Te',
                                    'district__icontains': 'gn'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gnome')
        self.assertNotContains(response, 'Valley')
        self.assertNotContains(response, 'Home')

    def test_content_type(self):
        response = self.client.get(reverse('record-list'), {})
        self.assertTrue('plain' in response.get('Content-Type', ''))



# Related images testing

class ImagesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        sp1 = Species.objects.create(name='Test')
        rec1 = Record.objects.create(species=sp1, district='Home')
        cls.im1 = Image.objects.create(order=0, title='greate image',
                                       description='full image description',
                                       src=SimpleUploadedFile('myimage.jpg',
                                                              b'this is file content'),
                                       record=rec1)
        cls.im2 = Image.objects.create(order=1, title='another image',
                                       description='Hello, testing is just at the beginning...',
                                       src=SimpleUploadedFile('theimage2.jpg',
                                                              b'another file content'),
                                       record=rec1)

    def test_all_images(self):
        rec = Record.objects.all()[0]
        self.assertEqual(rec.image_set.count(), 2)

    def test_reverse_relation(self):
        rec = Record.objects.all()[0]
        for im in Image.objects.all():
            self.assertEqual(rec, im.record)

    def tearDown(self):
         self.im1.src.delete()
         self.im2.src.delete()

# --------------- Species info tests

class SpeciesInfoTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.sp = Species.objects.create(name='Test',
                                        info='this is common information regarding the object')
        cls.client = Client()

    def test_response_ok(self):
        self.assertEqual(self.client.get(reverse('species-info', kwargs={'pk': 1}),
                                         {'pk': 1}).status_code, 200)

    def test_response_content(self):
        sp = Species.objects.all()[0]
        response = self.client.get(reverse('species-info', kwargs={'pk': sp.pk}), {'pk': sp.pk})
        self.assertContains(response, 'this is common')







