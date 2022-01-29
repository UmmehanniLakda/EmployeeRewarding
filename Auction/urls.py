from django.urls import path
from .views import create_task, task_list, task_detail, assign_task, assigned_tasks, my_assignment, create_submission, my_submission_list, task_submission_list, submission_accept

urlpatterns = [
    path('create/', create_task, name="create_task"),
    path('list/', task_list, name="task_list"),
    path('detail/<int:pk>/', task_detail, name="task_detail"),
    path('assign/<int:tpk>/<int:epk>/', assign_task, name="assign_task"),
    path('assigned/', assigned_tasks, name="assigned_tasks"),
    path('assigned/mytasks/', my_assignment, name="my_assignment"),
    path('submit/<int:pk>/', create_submission, name="create_submission"),
    path('submissions/my/<int:pk>', my_submission_list, name="my_submission_list"),
    path('submissions/task/<int:pk>', task_submission_list, name="task_submission_list"),
    path('submissions/task/detail/<int:pk>', submission_accept, name="submission_accept"),
]