"""Codeshala URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static
import Organization, Candidate, Auction, Voting, Leaderboard, Home
import Organization, Projects , Shoutout, Voting , Auction , Candidate, Chat

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('projects/', include('Projects.urls')),
    path('organization/', include('Organization.urls')),
    path('employee/', include('Candidate.urls')),
    path('auction/', include('Auction.urls')),
    path('shoutout/' , include('Shoutout.urls')),
    path('voting/', include('Voting.urls')),
    path('leaderboard/', include('Leaderboard.urls')),
    path('chat/', include('Chat.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)