from django.urls import path
from .views import org_create, org_login, org_architecture, team_create, org_create_project, org_project_accept, org_submission_list, parent_project_list, org_projects_list, org_team_create, user_logout


urlpatterns = [
    path('create/', org_create, name="org_create"),
    path('login/', org_login, name="org_login"),
    path('logout/', user_logout, name="logout"),
    path('designation/', org_architecture, name="org_architecture"),
    path('team_create/', team_create, name="team_create"),
    path('project/create/', org_create_project, name="org_create_project"),
    path('project/accept/<int:pk>/', org_project_accept, name="org_project_accept"),
    path('project/<int:pk>/list/', org_submission_list, name="org_submission_list"),
    path('project/parent/list/', parent_project_list, name="parent_project_list"),
    path('project/parent/<int:pk>/', org_projects_list, name="org_projects_list"),
    path('team/create/', org_team_create, name="org_team_create"),
]