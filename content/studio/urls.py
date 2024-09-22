from django.urls import path
from . import views


app_name = 'studio'
urlpatterns = [
    path('', views.index, name='index'), #type: ignore
    path('<str:obj>/', views.view, name='view'), #type: ignore
    path('<str:obj>/add/', views.add, name='add'), #type: ignore
    path('<str:obj>/<str:id>/edit/', views.edit, name='edit'), #type: ignore
    path('<str:obj>/<str:id>/delete/', views.delete, name='delete'), #type: ignore
]

