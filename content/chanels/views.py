from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Chanel

SUBSCRIBERS_MILESTONES = [1, 2, 3, 10, 20, 30]


def index(request):
    all_chanels = Chanel.objects.all().order_by('-date')
    return render(request, 'chanels/index.html', {'all_chanels':all_chanels})

def view(request, id):

    if request.method == 'GET':
        chanel = Chanel.objects.get(pk=id)
        subscribed = False
        if request.user.is_authenticated:
            if chanel in request.user.subscriptions.all():
                subscribed = True
        return render(request, 'chanels/view.html', {'chanel':chanel, 'subscribed':subscribed})

    elif request.method == 'POST':
        if request.user.is_authenticated:

            if request.POST.get('act') == 'subscribe':
                chanel = Chanel.objects.get(id=id)
                if request.user not in chanel.subscribers.all():
                    chanel.subscribers.add(request.user)
                    for i in range(len(SUBSCRIBERS_MILESTONES)):
                        if chanel.subs() == SUBSCRIBERS_MILESTONES[i] and chanel.subscribers_milestones < i+1:
                            for editor in chanel.editors():
                                editor.add_notification(f'Your chanel "{chanel.name}" already has {chanel.subs()} subscribers!',
                                                        reverse('chanels:view', args=[id]))
                            chanel.subscribers_milestones += 1
                            chanel.save()
                    return JsonResponse({'authenticated':True, 'subscribed':True, 'count':chanel.subs()})
                else:
                    chanel.subscribers.remove(request.user)
                    return JsonResponse({'authenticated':True, 'subscribed':False, 'count':chanel.subs()})

        return JsonResponse({'authenticated':False})
