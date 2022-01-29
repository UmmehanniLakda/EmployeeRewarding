from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static
from .views import shoutout_create , shoutout_comment , shoutout_like, comment_like

urlpatterns = [
    path('all/' , shoutout_create ,name = 'shoutout_create'),
    path('<int:spk>/likes' , shoutout_like , name = 'shoutout_like'),
    path('<int:spk>/details' , shoutout_comment , name= 'shoutout_comment'),
    path('<int:spk>/<int:cpk>/details' , comment_like , name= 'comment_like'),
   
]