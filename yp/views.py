from django.shortcuts import render
from content.chanels.models import Chanel
from content.videos.models import Video
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.conf import settings
from django.utils import timezone
import random

User = get_user_model()


def index(request):
    return render(request, 'yp/index.html')

def clear(request):
    if settings.DEBUG:
        for i in Chanel.objects.all():
            i.delete()
        for i in User.objects.all():
            i.delete()
    return redirect('/')

def restart(request):
    if settings.DEBUG and request.user.is_authenticated:
        imgs = ['https://i3.ytimg.com/vi/FkCxR3Iw4ng/maxresdefault.jpg', 'https://i3.ytimg.com/vi/hdOdRaDjYTg/maxresdefault.jpg', 'https://i3.ytimg.com/vi/BMFGWEEavTw/maxresdefault.jpg', 'https://i3.ytimg.com/vi/_peirypZ8vw/maxresdefault.jpg', 'https://i3.ytimg.com/vi/0A9HvZ4vz74/maxresdefault.jpg']
        urls = ['hdOdRaDjYTg', 'FkCxR3Iw4ng', 'BMFGWEEavTw', '_peirypZ8vw', '0A9HvZ4vz74']
        names = ['Super Cool Video', 'New Video', 'Best Video Ever', 'minecraft playthrough', 'you laugh you loose', 'west side, my homies, beach', 'bruh', 'How To Cook Good Code', 'how to cook bad code', 'video', 'video n69', 'r34', 'never gonna give you up', 'never gonna let you down', 'nice video']
        for i in Chanel.objects.all():
            i.delete()
        new_chanel = Chanel(
                name='New Chanel',
                desc='Cool Chanel Description where I can tell you all about this lil chanel, what we do here and why you should subscribe',
                img='http://clipart-library.com/img1/689289.gif',
                owner=request.user,
                id='chanel-id',
                )
        new_chanel.save()
        for i in range(15):
            new_video = Video(
                    name=random.choice(names),
                    desc='This is video description, where I\'ll tell ya all about it and why you shuld definetly watch it and smash it a like',
                    url=random.choice(urls),
                    img=random.choice(imgs),
                    chanel=new_chanel,
                    date=timezone.now(),
                    id=i,
                    )
            new_video.save()
            new_video.authors.add(request.user)
    return redirect('/')

