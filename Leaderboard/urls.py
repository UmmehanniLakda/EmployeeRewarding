from django.urls import path
from .views import weekly_lead, yearly_lead, quaterly_lead, points_chart, points_chart_data, teams_charts_data, teams_chart, emp_progress, emp_progress_chart

urlpatterns = [
    path('weekly/', weekly_lead, name="weekly_lead"),
    path('yearly/', yearly_lead, name="yearly_lead"),
    path('quarter/', quaterly_lead, name="quaterly_lead"),
    path('charts/points/', points_chart, name="points_chart"),
    path('charts/teams/', teams_chart, name="teams_chart"),
    path('charts/employee/', emp_progress_chart, name="emp_progress_chart"),
    path('data/points/', points_chart_data, name="points_chart_data"),
    path('data/teams/', teams_charts_data, name="teams_charts_data"),
    path('data/employee/', emp_progress, name="emp_progress"),
]

    