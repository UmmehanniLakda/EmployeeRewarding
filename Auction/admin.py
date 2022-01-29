from django.contrib import admin
from .models import Task, Taskassigned, Tasksubmission, Tasksubmissionfile
# Register your models here.

admin.site.register(Task)
admin.site.register(Taskassigned)
admin.site.register(Tasksubmission)
admin.site.register(Tasksubmissionfile)
