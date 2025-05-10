from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',  auth_views.LoginView.as_view(template_name='upload/login.html'),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'),                 name='logout'),

     path('', views.home,name='home'), 
    path('upload/file/', views.upload_file, name='upload_file'),
    path('upload/image/', views.upload_image, name='upload_image'),
    path('my-uploads/', views.my_uploads, name='my_uploads'),
    path('api/autocomplete_titles/', views.autocomplete_titles, name='autocomplete_titles'),
]
