from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'), #type: ignore
    path('me/', views.me, name='me'), #type: ignore
    path('reg/', views.register, name='register'), #type: ignore
    path('login/', views.user_login, name='login'), #type: ignore
    path('logout/', views.user_logout, name='logout'), #type: ignore
    path('notifications/', views.notifications, name='notifications'), #type: ignore
    path('is_authenticated/', views.is_authenticated, name='is_authenticated'), #type: ignore
    path('verify/<str:username>/<str:token>/', views.verify, name='verify'),
    path('resend_verification/', views.resend_verification, name='resend_verification'),
    path('@<str:username>/', views.view, name='view'), #type: ignore
]


