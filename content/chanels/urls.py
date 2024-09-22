from django.urls import path

from . import views


app_name = 'chanels'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:id>/', views.view, name='view'), #type:ignore
]
