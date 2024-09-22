from django import forms
from content.videos.models import Video
from content.chanels.models import Chanel
from social.users.models import Notification
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid

User = get_user_model()


class VideoForm(forms.ModelForm):

    chanel = forms.CharField(label='Chanel:')
    authors = forms.CharField(label='Authors:')

    class Meta: #type:ignore
        model = Video
        fields = ['name', 'desc', 'url', 'img']


    def clean_chanel(self):
        name = self.cleaned_data['chanel']
        if Chanel.objects.filter(name=name).exists():
            chanel = Chanel.objects.get(name=name)
            return chanel
        else:
            self.add_error('chanel', f'{name} is not found')
            return

    def clean_authors(self):
        data = self.cleaned_data['authors']
        authors = []
        data = data.replace(' ', '')
        usernames = list(data.split(','))
        for username in usernames:
            if User.objects.filter(username=username).exists():
                new_author = User.objects.get(username=username)
                authors.append(new_author)
            else:
                self.add_error('authors', f'Admin not found: {username}')
        if len(authors) < 1:
            self.add_error('authors', 'Video should have at least one author')
        return authors


    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        instance = kwargs.pop('obj', None)
        super(VideoForm, self).__init__(*args, **kwargs)
        if instance:
            self.fields['url'].disabled = True
            self.fields['chanel'].disabled = True
            self.fields['authors'].disabled = True
            self.fields['chanel'].initial = instance.chanel.name
            self.fields['authors'].initial = ', '.join(instance.authors.all().values_list('username', flat=True))
        else:
            self.fields['authors'].initial = request.user.username


    def save(self, commit=True):
        instance = super().save(commit=False)
        is_new = not instance.id
        if is_new:
            instance.chanel = self.cleaned_data['chanel']
            instance.id = str(uuid.uuid4().hex)[:12]
        instance.save()
        if is_new:
            instance.authors.set(self.cleaned_data['authors'])
            for sub in instance.chanel.subscribers.all():
                sub.add_notification(
                    text=f'On chanel "{instance.chanel.name}" there is a new video "{instance.name}"!',
                    url=reverse('videos:view', args=[instance.id])
                )
        return instance




class ChanelForm(forms.ModelForm):

    owner = forms.CharField(label='Owner:')
    admins = forms.CharField(label='Admins:', required=False)

    class Meta: #type:ignore
        model = Chanel
        fields = ['name', 'desc', 'img']


    def clean_owner(self):
        username = self.cleaned_data['owner']
        if User.objects.filter(username=username).exists():
            owner = User.objects.get(username=username)
            return owner
        else:
            self.add_error('owner', f'{username} is not found')
            return


    def clean_admins(self):
        data = self.cleaned_data['admins']
        admins = []
        if data:
            data = data.replace(' ', '')
            usernames = list(data.split(','))
            for username in usernames:
                if User.objects.filter(username=username).exists():
                    new_admin = User.objects.get(username=username)
                    owner = self.cleaned_data['owner']
                    if new_admin == owner:
                        self.add_error('admins', f"{owner} is the chanel's owner. He can't be an admin")
                    else:
                        admins.append(new_admin)
                else:
                    self.add_error('admins', f'Admin not found: {username}')
        return admins


    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        instance = kwargs.pop('obj', None)
        super(ChanelForm, self).__init__(*args, **kwargs)
        if instance:
            self.fields['owner'].initial = instance.owner.username
            self.fields['admins'].initial = ', '.join(instance.admins.all().values_list('username', flat=True))
            if request.user != instance.owner:
                self.fields['owner'].disabled = True
                self.fields['admins'].disabled = True
        else:
            self.fields['owner'].initial = request.user
            self.fields['owner'].disabled = True


    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.id:
            instance.id = str(uuid.uuid4().hex)[:12]
        instance.owner = self.cleaned_data['owner']
        instance.save()
        instance.admins.set(self.cleaned_data['admins'])
        return instance



class DeleteForm(forms.Form):
    class Meta: #type:ignore
        fields = []
