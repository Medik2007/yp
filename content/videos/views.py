from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Video
from .models import Comment
import content.chanels.views as chanels_views

LIKES_MILESTONES = [1, 2, 3, 10, 20, 30]

def send_notifications(text, editors, id):
    for editor in editors: 
        editor.add_notification( #type:ignore
            text,
            reverse('videos:view', args=[id]))

def send_likes_notifications(instance, id):
    for i in range(len(LIKES_MILESTONES)):
        if instance.likes() == LIKES_MILESTONES[i] and instance.likes_milestones < i+1:
            if type(instance) == Video:
                send_notifications(f'Your video "{instance.name}" already has {instance.likes()} likes!', instance.editors(), id)
            elif type(instance) == Comment:
                send_notifications(f'Your comment on video "{instance.video.name}" already has {instance.likes()} likes!', instance.editors(), id)
            instance.likes_milestones += 1
            instance.save()
        elif i > instance.likes():
            break


def index(request):
    videos = Video.objects.all().order_by('-date')
    return render(request, 'videos/index.html', {'videos':videos})

def view(request, id):

    if request.method == 'GET':
        video = Video.objects.get(id=id)
        subscribed = False
        if request.user.is_authenticated:
            if video.chanel in request.user.subscriptions.all():
                subscribed = True
        other_videos = []
        all_videos = Video.objects.all()
        for i in range(4):
            other_videos.append(all_videos[i])
        comments = video.comments.filter(parent=None) #type: ignore
        return render(request, 'videos/view.html', {'video':video, 'comments':comments, 'subscribed':subscribed, 'other_videos':other_videos})

    elif request.method == 'POST':
        if request.user.is_authenticated:


            if request.POST.get('act') == 'like':
                if request.POST.get('model') == 'video':
                    instance = Video.objects.get(id=id)
                    instance_id = 'object'
                else:
                    instance_id = request.POST.get('id')
                    instance = Comment.objects.get(id=instance_id)
                if not instance.liked_users.filter(username=request.user.username).exists():
                    instance.liked_users.add(request.user)
                    send_likes_notifications(instance, id)
                    return JsonResponse({'authenticated':True, 'liked':True, 'count':instance.likes(), 'id':instance_id})
                else:
                    instance.liked_users.remove(request.user)
                    return JsonResponse({'authenticated':True, 'liked':False, 'count':instance.likes(), 'id':instance_id})


            elif request.POST.get('act') == 'subscribe':
                video = Video.objects.get(id=id)
                return chanels_views.view(request, video.chanel.id)


            elif request.POST.get('act') == 'comment':
                video = Video.objects.get(id=id)
                parent_id = 'object'
                if request.POST.get('parent'):
                    parent = Comment.objects.get(id=request.POST['parent'])
                    parent_id = parent.pk
                    comment = Comment(text=request.POST['text'], author=request.user, video=video, parent=parent)
                    send_notifications(f'Someone has answered on your comment under the video "{parent.video.name}"', parent.editors(), id)
                else:
                    comment = Comment(text=request.POST['text'], author=request.user, video=video)
                    send_notifications(f'There is a new comment under your video "{video.name}"', video.editors(), id)
                comment.save()
                return JsonResponse({'authenticated':True, 'author':request.user.username, 'id':comment.pk, 'parent':parent_id})


            elif request.POST.get('act') == 'edit':
                comment = Comment.objects.get(id=request.POST.get('id'))
                if request.user == comment.author:
                    text = request.POST.get('text')
                    if text.replace(' ', '') != '':
                        comment.text = text
                        comment.save()
                        return JsonResponse({'authenticated':True, 'id':comment.pk})


            elif request.POST.get('act') == 'delete':
                comment = Comment.objects.get(id=request.POST.get('id'))
                if request.user == comment.author:
                    id = comment.pk
                    comment.delete()
                    return JsonResponse({'authenticated':True, 'id':id})

        return JsonResponse({'authenticated':False})
