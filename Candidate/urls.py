from django.urls import path
from .views import emp_create, emp_design, emp_child_list, emp_login, emp_setchild


urlpatterns = [
    path('create/', emp_create, name="emp_create"),
    path('login/', emp_login, name="emp_login"),
    path('design/', emp_design, name="emp_design"),
    path('children/', emp_child_list, name="emp_child_list"),
    path('children/<int:pk>/', emp_setchild, name="emp_setchild"),
]