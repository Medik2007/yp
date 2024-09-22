from django.test import TestCase
from django.urls import reverse
from content.studio.tests import add_chanel, get_response_test

class VideoTest(TestCase):

    def test_view(self):
        print('CHANELS: Testing Chanels View page')
        chanel = add_chanel(self)

        # Testing GET response
        get_response_test(self, reverse('chanels:view', args=[chanel.id]), 'chanels/view.html')

    def test_index(self):
        print('.CHANELS: Testing Chanels Index page')
        add_chanel(self)
        add_chanel(self)
        add_chanel(self)
        add_chanel(self)

        # Testing GET response
        get_response_test(self, reverse('chanels:index'), 'chanels/index.html')


