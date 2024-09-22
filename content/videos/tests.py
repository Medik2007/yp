from django.test import TestCase
from django.urls import reverse
from content.studio.tests import add_video, get_response_test

class VideoTest(TestCase):

    def test_view(self):
        print('VIDEOS: Testing Videos View page')
        video = add_video(self)

        # Testing GET response
        get_response_test(self, reverse('videos:view', args=[video.id]), 'videos/view.html')

    def test_index(self):
        print('VIDEOS: Testing Videos Index page')
        add_video(self)
        add_video(self)
        add_video(self)
        add_video(self)

        # Testing GET response
        get_response_test(self, reverse('videos:index'), 'videos/index.html')


