from django.test import TestCase
from django.urls import reverse

# Import your model and form
from content.videos.models import Video
from content.chanels.models import Chanel
import content.studio.forms as forms


class VideoTest(TestCase):

    def asadsed(self):
        get_response_test(self, reverse('studio:add', args=['v']), 'studio/form.html', forms.VideoForm)
        add_video(self)
        data = {'name':' ', 'desc':'This is an invalid test description', 'url':'asd'}
        invalid_add_test(self, data, Video, 'v', 1)

    def sdsd(self):
        print("STUDIO: Testing Edit Video functionality")
        video = add_video(self)

        # Test GET edit response
        get_response_test(self, reverse('studio:edit', args=['v', video.id]), 'studio/form.html', forms.video.edit)

        # Test POST response and edit video
        data = {'name': 'New video name', 'desc': 'This is a new description', 'url': 'https://new-example.com/'}
        edited = edit_test(self, data, Video, 'v', 1, video)

        # Test edit with invalid data
        data = {'name': ' ', 'desc': 'Invalid edited description'}
        invalid_edit_test(self, data, Video, 'v', 1, edited)




















def get_response_test(self, url, template, form=None):
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, template)
    if form: self.assertIsInstance(response.context['form'], form)
    return response

def add_test(self, data, obj, obj_type, count):
    response = self.client.post(reverse('studio:add', args=[obj_type]), data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'success': True})
    if count != False: self.assertEqual(obj.objects.count(), count)
    self.assertEqual(obj.objects.last().name, data['name'])

def invalid_add_test(self, data, obj, obj_type, count):
    response = self.client.post(reverse('studio:add', args=[obj_type]), data)
    self.assertEqual(response.status_code, 200)
    self.assertNotEqual(response.json(), {'success': True})
    self.assertEqual(obj.objects.count(), count)

def edit_test(self, data, obj, obj_type, count, original):
    response = self.client.post(reverse('studio:edit', args=[obj_type, original.id]), data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'success': True})
    self.assertEqual(obj.objects.count(), count)
    edited = obj.objects.get()
    self.assertEqual(edited.name, data['name'])
    self.assertEqual(edited.desc, data['desc'])
    self.assertEqual(edited.id, original.id)
    return edited

def invalid_edit_test(self, data, obj, obj_type, count, original):
    response = self.client.post(reverse('studio:edit', args=[obj_type, original.id]), data)
    self.assertEqual(response.status_code, 200)
    self.assertNotEqual(response.json(), {'success':True})
    self.assertEqual(obj.objects.count(), count)
    wrong_edit = obj.objects.get()
    self.assertEqual(wrong_edit.name, original.name)
    self.assertEqual(wrong_edit.desc, original.desc)
    self.assertEqual(wrong_edit.id, original.id)

def delete_test(self, obj_type, original, count):
    response = self.client.post(reverse('studio:delete', args=[obj_type, original.id]), {})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'success': True})
    self.assertEqual(Video.objects.count(), count)


def add_chanel(self):
    data = {'name':'Chanel Name', 'desc':'Desctoption'}
    add_test(self, data, Chanel, 'c', False)
    return Chanel.objects.all()[Chanel.objects.count()-1]

def add_video(self):
    chanel = add_chanel(self)
    data = {'name': 'Test Video', 'desc': 'This is a test description', 'url': 'https://example.com/video', 'chanel':chanel.id}
    add_test(self, data, Video, 'v', False)
    return Video.objects.all()[Video.objects.count()-1]




class asd(TestCase):

    def asadsed(self):
        print("STUDIO: Testing Add Video functionality")

        # Test GET response
        get_response_test(self, reverse('studio:add', args=['v']), 'studio/form.html', forms.video.add)

        # Test POST response and add video
        add_video(self)

        # Test adding video with invalid data
        data = {'name':' ', 'desc': 'This is an invalid test description'}
        invalid_add_test(self, data, Video, 'v', 1)

    def sdsd(self):
        print("STUDIO: Testing Edit Video functionality")
        video = add_video(self)

        # Test GET edit response
        get_response_test(self, reverse('studio:edit', args=['v', video.id]), 'studio/form.html', forms.video.edit)

        # Test POST response and edit video
        data = {'name': 'New video name', 'desc': 'This is a new description', 'url': 'https://new-example.com/'}
        edited = edit_test(self, data, Video, 'v', 1, video)

        # Test edit with invalid data
        data = {'name': ' ', 'desc': 'Invalid edited description'}
        invalid_edit_test(self, data, Video, 'v', 1, edited)

    def asd(self):
        print("STUDIO: Testing Delete Video functionality")
        video = add_video(self)

        # Test GET delete response
        get_response_test(self, reverse('studio:delete', args=['v', video.id]), 'studio/form.html', forms.video.delete)

        # Test POST delete response and delete the video
        delete_test(self, 'v', video, 0)



class dsa(TestCase):

    def sd(self):
        print("STUDIO: Testing Add Chanel functionality")

        # Test GET response
        get_response_test(self, reverse('studio:add', args=['c']), 'studio/form.html', forms.chanel.add)

        # Test POST response and add video
        add_chanel(self)

        # Test adding video with invalid data
        data = {'name':' ', 'desc': 'This is an invalid test description'}
        invalid_add_test(self, data, Chanel, 'c', 1)

    def dsa(self):
        print("STUDIO: Testing Edit Chanel functionality")
        chanel = add_chanel(self)

        # Test GET edit response
        get_response_test(self, reverse('studio:edit', args=['c', chanel.id]), 'studio/form.html', forms.chanel.edit)

        # Test POST response and edit video
        data = {'name': 'New video name', 'desc': 'This is a new description'}
        edited = edit_test(self, data, Chanel, 'c', 1, chanel)

        # Test edit with invalid data
        data = {'name': ' ', 'desc': 'Invalid edited description'}
        invalid_edit_test(self, data, Chanel, 'c', 1, edited)

    def asd(self):
        print("STUDIO: Testing Delete Chanel functionality")
        chanel = add_chanel(self)

        # Test GET delete response
        get_response_test(self, reverse('studio:delete', args=['c', chanel.id]), 'studio/form.html', forms.chanel.delete)

        # Test POST delete response and delete the video
        delete_test(self, 'c', chanel, 0)
