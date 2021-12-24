from django.urls import path
from . import views

urlpatterns = [
    # path('upload_folder', views.upload_folder),
    # path('mkdir', views.mkdir),
    # path('upload_file', views.upload_file),
    # path('download_file', views.download_file),

    path('', views.index),
    path('delete_file/', views.delete_file),
    path('download_file/', views.download_file),
    path('upload_file/', views.upload_file),
    path('file_type/', views.file_type),
    path('search/', views.search),
    # path('login/', views.login),
    # path('logout/', views.logout),
    # path('register/', views.register),
    path('folder/', views.folder),
    path('mkdir/', views.mkdir),
    path('delete_folder/', views.delete_folder),
    path('rename_file/', views.rename_file),
    path('rename_folder/', views.rename_folder),
    path('mkdir_pro_cli_time', views.mkdir_pro_cli_time),
]