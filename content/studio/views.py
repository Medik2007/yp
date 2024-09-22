from django.http import Http404
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from content.videos.models import Video
from content.chanels.models import Chanel
from content.studio.forms import VideoForm, ChanelForm, DeleteForm

get_obj = {
    'c':{'model':Chanel, 'form':ChanelForm, 'name':'Chanel', 'redirect':'chanels:view'},
    'v':{'model':Video,  'form':VideoForm,  'name':'Video',  'redirect':'videos:view'},
} 
def get_redirect(obj, id): return reverse(get_obj[obj]['redirect'], args=[id]) #type:ignore



def check_obj(function):
    def wrapper(request, *args, **kwargs):
        if kwargs['obj'] in get_obj.keys():
            return function(request, *args, **kwargs)
        raise Http404
    return wrapper

def check_authority(function):
    def wrapper(request, *args, **kwargs):
        model = get_obj[kwargs['obj']]['model']
        instance = get_object_or_404(model, id=kwargs['id'])
        if request.user in instance.editors():
            kwargs['instance'] = instance
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper



@login_required
def index(request):
    return render(request, 'studio/index.html')



@login_required #type:ignore
@check_obj
def view(request, obj):
    all_obj = []
    if obj == 'c':
        for admin in request.user.admin_chanels.all():
            all_obj.append(admin)
        for owner in request.user.owner_chanels.all():
            all_obj.append(owner)
    elif obj == 'v':
        all_obj = request.user.videos.all().order_by('-date')
    return render(request, 'studio/view.html', {'all_obj':all_obj, 'type':obj})



@login_required #type:ignore
@check_obj
def add(request, obj, chanel=None):
    form = get_obj[obj]['form']

    if request.method == 'GET':
        initial = {}
        data = request.GET.dict()
        if obj != 'c' and 'chanel' in data and Chanel.objects.filter(name=data['chanel']).exists():
            chanel = Chanel.objects.get(name=data['chanel'])
            initial = {'chanel':chanel.name}
        return render(request, 'studio/form.html', {'form':form(request=request, initial=initial)})

    elif request.method == 'POST':
        result = form(request.POST, request=request)
        if result.is_valid():
            instance = result.save()
            return JsonResponse({'success':True, 'name':get_obj[obj]['name'], 'redirect':True, 'link':get_redirect(obj, instance.id)})
        else:
            return JsonResponse({'success':False, 'errors':result.errors})



@login_required #type:ignore
@check_obj
@check_authority
def edit(request, obj, id, instance):
    form = get_obj[obj]['form']

    if request.method == 'GET':
        return render(request, 'studio/form.html', {'form':form(request=request, obj=instance, instance=instance)})

    elif request.method == 'POST':
        result = form(request.POST, request=request, obj=instance, instance=instance)
        if result.is_valid():
            result.save()
            return JsonResponse({'success':True, 'name':get_obj[obj]['name'], 'redirect':False, 'link':get_redirect(obj, id)})
        else:
            return JsonResponse({'success':False, 'errors':result.errors})



@login_required #type:ignore
@check_obj
@check_authority
def delete(request, obj, id, instance):

    if request.method == 'GET':
        return render(request, 'studio/form.html', {'form':DeleteForm()})

    elif request.method == 'POST':
        result = DeleteForm(request.POST)
        if result.is_valid():
            instance.delete()
            return JsonResponse({'success':True, 'redirect':True, 'link':reverse('studio:view', args=[obj])})
        else:
            return JsonResponse({'success':False, 'errors':result.errors})
