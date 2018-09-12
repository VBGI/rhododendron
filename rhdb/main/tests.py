from django.test import TestCase, TransactionTestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Species, Image, Record, Page
from .filters import RecordFilter
from django.urls import reverse


# ------- test constants --------------

# attributes for testing

species_allowed_attributes = ('name', 'info', 'created', 'updated')

record_allowed_attributes = ('species', 'updated', 'created', 'region',
                             'district', 'content', 'latitude', 'longitude')

image_allowed_attributes = ('description', 'title', 'created', 'updated',
                             'src', 'record', 'order', 'category',
                            'category_slug', 'category_name')

page_allowed_attrs = ('public','content', 'title', 'order')

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

    def test_not_contain_google_maps(self):
        response = self.client.get(reverse('record-list'),
                                   {'species__name__icontains': 'Te',
                                   'district__icontains': 'gn'})
        self.assertNotContains(response, 'map.js')


    def test_content_type(self):
        response = self.client.get(reverse('record-list'), {})
        self.assertTrue('html' in response.get('Content-Type', ''))

    def test_list_record_template(self):
        response = self.client.get(reverse('record-list'), {})
        self.assertContains(response, 'Последнее изменение')

# ---------------- Record details
class RecordDetailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        sp1 = Species.objects.create(name='Test', info='spinfo')
        cls.rec = Record.objects.create(species=sp1, district='Home',
                                        region='one_region',
                                        content='simplified_content')
        Page.objects.create(title='yet_another_title1', public=True)
        Page.objects.create(title='yet_another_title2', public=True)
        cls.client = Client()

    def test_record_detail_status(self):
        response = self.client.get(reverse('record-info', kwargs={'pk': self.rec.pk}))
        self.assertEqual(response.status_code, 200)

    def test_record_complex(self):
        response = self.client.get(
            reverse('record-info', kwargs={'pk': self.rec.pk}))
        self.assertContains(response, 'Home')
        self.assertContains(response, 'one_region')
        self.assertContains(response, 'simplified_content')
        self.assertContains(response, 'spinfo')
        self.assertContains(response, 'Test')

    def test_pages_render(self):
        response = self.client.get(
            reverse('record-info', kwargs={'pk': self.rec.pk}))
        self.assertContains(response, 'yet_another_title1')
        self.assertContains(response, 'yet_another_title2')


# ---------------- 0 Related images testing
class ImagesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        sp1 = Species.objects.create(name='Test')
        rec1 = Record.objects.create(species=sp1, district='Home')
        cls.rec = rec1
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
        cls.im3 = Image.objects.create(order=2, title='new image',
                                       description='',
                                       src=SimpleUploadedFile('newimage.jpg',
                                                              b'content'))
        cls.client = Client()

    def test_all_images(self):
        self.assertEqual(self.rec.image_set.count(), 2)

    def test_related_images(self):
        res = self.rec.image_set.all()
        self.assertEqual(len(res), 2)
        self.assertNotIn(self.im3, res)

    def test_related_view_type(self):
        response = self.client.get(reverse('list-images', kwargs={'pk': self.rec.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('json' in response.get('Content-Type', ''))

    def test_reslate_view_content(self):
        response = self.client.get(reverse('list-images', kwargs={'pk': self.rec.pk}))
        self.assertContains(response, self.im1.title)
        self.assertContains(response, self.im2.title)

    def tearDown(self):
        self.im1.src.delete()
        self.im2.src.delete()
        self.im3.src.delete()


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


# ----------------- Page attributes auto-tests
class PageAttributesTests(metaclass=auto_attr_helper('page',
                                                     *page_allowed_attrs)):
    @classmethod
    def setUpTestData(cls):
        cls.page = Page.objects.create(title='unique title',
                                       content='another content',
                                       public=True)
        cls.client = Client()

    def test_page_generated(self):
        response = self.client.get(reverse('page-info', kwargs={'pk': self.page.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'unique title')
        self.assertContains(response, 'another content')


# -------------- Context processor testing
class SpeciesInfoTest(TestCase):
    pass


# ------------- Base detials & rendering

class BaseDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.page = Page.objects.create(title='unique_title', public=True)
        cls.client = Client()

    def test_base_page_status(self):
        response = self.client.get(reverse('base-view'))
        self.assertEqual(response.status_code, 200)

    def test_base_content(self):
        response = self.client.get(reverse('base-view'))
        self.assertContains(response, 'unique_title')
        self.assertContains(response, 'Rhododendron')

    def test_google_map_included(self):
        response = self.client.get(reverse('base-view'))
        self.assertContains(response, 'map.js')
