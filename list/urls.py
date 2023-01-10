from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('view-<id>/', views.view, name='view'),
    path('create/', views.create, name='create'),
    path('edit-<id>/', views.edit, name='edit'),
    path('delete-<id>/', views.delete, name='delete'),
    path('complete-<id>/', views.complete, name='complete'),
    path('search/', views.search, name='search'),
]