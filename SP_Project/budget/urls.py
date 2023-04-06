
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='list'),
    path('', views.project_list, name='list'),
    path('add/', views.ProjectCreateView.as_view(), name='add'),
    path('<slug:project_slug>', views.project_detail, name='detail'),
    path('Group/', views.group, name='group'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('export_csv', views.export_csv, name='export_csv'),
]
