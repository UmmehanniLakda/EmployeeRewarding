from django.db import models
from django.contrib.auth.models import User
from Client.models import Emp as Employee

# Create your models here.

class Task(models.Model):
    name = models.TextField()
    description = models.TextField()
    creator = models.ForeignKey(Employee, on_delete=models.CASCADE , default=1)
    max_reward = models.IntegerField()
    assigned = models.BooleanField(default=False, editable=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(blank=True)
    deadline = models.DateTimeField()
    completed = models.BooleanField(default=False, editable=True)

class Taskassigned(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,default=1)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE , default=1)
    bid_points = models.IntegerField()
    status = models.BooleanField(default=False, editable=True)
    asignment_time = models.DateTimeField(auto_now_add=True)

class Tasksubmission(models.Model):
    assignment = models.ForeignKey(Taskassigned, on_delete=models.CASCADE , default=1)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE , default=1)
    accepted = models.BooleanField(default=False, editable=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    description = models.TextField(blank=True)

class Tasksubmissionfile(models.Model):
    submission = models.ForeignKey(Tasksubmission, on_delete=models.CASCADE , default=1)
    file_item = models.FileField(upload_to='submission')

class Taskbid(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE , default=1)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE , default=1)
    bid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)



