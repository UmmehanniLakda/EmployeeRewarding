from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static
from .views import create_project , submit_project , accept_project , display_project , list_project , assigned_project


urlpatterns = [
    path('create/' , create_project , name = "create_project"),
    path('all/' , display_project , name = "display_project"),
    path('assigned/' , assigned_project , name = 'assigned_project'),
    path('<int:ppk>/list/' , list_project , name = "list_project"),
    path('<int:ppk>/<int:tpk>/submit/' , submit_project , name = "submit_project"),
    path('<int:ppk>/<int:cpk>/accept/' , accept_project , name = "accept_project"),
]