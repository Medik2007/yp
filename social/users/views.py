from django.contrib.auth import authenticate, login, get_user_model, logout
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.urls import reverse
from .forms import RegisterForm, LoginForm

from datetime import datetime
from datetime import timedelta

import secrets
import hashlib

User = get_user_model()

def index(request):
    all_users = User.objects.all()
    return render(request, 'users/index.html', {'all_users':all_users})

def view(request, username):
    user = User.objects.get(username=username)
    the_user = False
    if request.user == user: the_user = True
    return render(request, 'users/view.html', {'user':user, 'the_user':the_user})

def me(request):
    if request.user.is_authenticated:
        return redirect(reverse('users:view', args=[request.user.username]))
    else:
        return redirect(reverse('users:login'))


@require_POST
def is_authenticated(request):
    return JsonResponse({'is_authenticated':request.user.is_authenticated})

@login_required
@require_POST
def notifications(request):

    if request.POST.get('act') == 'number':
        return JsonResponse({'number':request.user.notifications.filter(is_watched=False).count()})

    elif request.POST.get('act') == 'get':
        if request.user.notifications.all():
            notifications = [[],[]]
            new = request.user.notifications.filter(is_watched=False)
            old = request.user.notifications.filter(is_watched=True)
            for i in old:
                notifications[1].append([i.text, i.url])
            for i in new:
                notifications[0].append([i.text, i.url])
                i.is_watched = True
                i.save()
            for i in notifications:
                i.reverse()
            if notifications:
                return JsonResponse({'notifications':notifications})
        return JsonResponse({'notifications':False})

    elif request.POST.get('act') == 'clear':
        for notif in request.user.notifications.all(): notif.delete()
        return JsonResponse({'success':True})


def send_verification(user):
    token = secrets.token_urlsafe(32)
    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    user.verification_token = hashed_token
    user.verification_sent = datetime.now()
    user.save()

    verification_url = reverse('users:verify', args=[user.username, token])
    send_mail(
        'Email Verification on Young Planet',
        f': http://127.0.0.1:8000{verification_url}',
        'meeedik2007@gmail.com',
        [user.email],
    )


def verify(request, username, token):
    user = get_object_or_404(User, username=username)
    if not user.is_verified: #type: ignore
        if hashlib.sha256(token.encode()).hexdigest() == user.verification_token: #type: ignore
            if str(datetime.now()) < str(user.verification_sent + timedelta(days=1)): #type: ignore
                user.is_verified = True #type: ignore
                user.save()
                login(request, user)
                return render(request, 'users/verify.html', {'profile':reverse('users:view', args=[user.username])}) #type: ignore
            else:
                send_verification(user)
                return render(request, 'users/verify.html', {'expired':True})
    raise Http404


@require_POST
def resend_verification(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if not user.is_verified: #type: ignore
        if str(user.verification_sent + timedelta(minutes=5)) > str(datetime.now()): #type: ignore
            return JsonResponse({'sent':False})
        send_verification(user)
        return JsonResponse({'sent':True})



def register(request):

    if request.method == 'GET':
        if request.user.is_anonymous:
            return render(request, 'users/form.html', {'form':RegisterForm})
        else:
            return redirect(reverse('users:view', args=[request.user.username]))

    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User(username=data['username'], email=data['email'], img=data['img'])
            user.set_password(data['password'])
            user.save()
            send_verification(user)
            return JsonResponse({'success':False, 'errors':{'Email Verification':'On your Email was sent a letter to verify your Email Address. Please follow the instructions in that letter.'}})
        return JsonResponse({'success':False, 'errors':form.errors})



def user_login(request):

    if request.method == 'GET':
        if request.user.is_anonymous:
            return render(request, 'users/form.html', {'form':LoginForm})
        else:
            return redirect(reverse('users:view', args=[request.user.username]))

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                if user.is_verified: #type:ignore
                    login(request, user)
                    return JsonResponse({'success':True, 'redirect':True, 'link':reverse('users:view', args=[user.username])}) #type:ignore
                return JsonResponse({'success':False, 'errors':{'Email Validation':'You should verify your Email before Logging into the site. We have sent you a letter with instructions to verify your Email Address.'}})
            return JsonResponse({'success':False, 'errors':{'Error':'Invalid username or password'}})
        return JsonResponse({'success':False, 'errors':form.errors})



@login_required #type:ignore
def user_logout(request):
    if request.method == 'GET':
        return render(request, 'users/form.html')
    elif request.method == 'POST':
        logout(request)
        return JsonResponse({'success':True, 'redirect':True, 'link':'/'}) #type:ignore

