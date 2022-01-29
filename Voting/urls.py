from django.urls import path
from .views import teams_all, team_vote

urlpatterns = [
    path('teams/all', teams_all, name="teams_all"),
    path('teams/<int:pk>', team_vote, name="team_vote"),
]