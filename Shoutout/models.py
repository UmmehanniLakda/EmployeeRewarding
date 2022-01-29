from django.db import models
from django.contrib.auth.models import User
from Client.models import Emp , Organization
# Create your models here.

class Shoutout(models.Model):
    description = models.TextField(max_length=200)
    emp_appreciator = models.ForeignKey(User , on_delete=models.CASCADE , blank=True , null=True)
    emp_appreciated = models.ForeignKey(Emp , on_delete=models.CASCADE , blank=True , null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization , on_delete=models.CASCADE , blank=True , null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='shoutoutlikes')

class Comment(models.Model):
    comment = models.TextField(blank=True , null=True , default='' , editable=True)
    shoutout = models.ForeignKey(Shoutout , on_delete=models.CASCADE)
    emp_commented = models.ForeignKey(User , on_delete = models.CASCADE , default='')
    likes = models.ManyToManyField(User , blank=True, related_name='commentlikes')
    timestamp = models.DateTimeField(auto_now_add=True)