# urls.py
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.ipCheck, name='ipCheck'),
    path('index/', views.ipCheck, name='ipCheck'),
    path('auth/', views.auth, name='auth'),
    path('home/', views.home, name='home'),
    path('folder/', views.folder, name='folder'),
    path('upload-folder/', views.upload_folder, name='upload_folder'),
    path('get-files/', views.get_files, name='get_files'),
    path('download-file/', views.download_file, name='download_file'),
    path('upload-file/', views.upload_file, name='upload_file'),

]
