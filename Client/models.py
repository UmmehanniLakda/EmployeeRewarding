from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=100, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False, editable=True)
    desigset = models.BooleanField(default=False, editable=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ParentProject(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.TextField()

class Designation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    designation = models.TextField()
    priority = models.IntegerField()

    def __str__(self):
        return self.designation

class Emp(models.Model):
    name = models.CharField(max_length= 50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , default='')
    doj = models.DateTimeField(auto_now_add = True)
    doj_testing = models.DateTimeField(null=True, blank=True)
    dob = models.DateTimeField()
    age = models.IntegerField(null=True)
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    points = models.IntegerField()
    designation = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Parent(models.Model):
    emp = models.OneToOneField(Emp, on_delete = models.CASCADE)

    def __str__(self):
        return self.emp.name


class Child(models.Model):
    emp = models.OneToOneField(Emp, on_delete = models.CASCADE)
    parent = models.ManyToManyField(Parent, blank=True)

    def __str__(self):
        return self.emp.name


class Team(models.Model):
    parent = models.ForeignKey(Parent, on_delete = models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE, null=True, blank=True)
    child = models.ManyToManyField(Child)
    name = models.CharField(max_length=50)

    def str(self):
        return self.name


class Project(models.Model):
    parentproject = models.ForeignKey(ParentProject, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20 , blank=True , null=True)
    description = models.CharField(max_length=500)
    default_pts = models.IntegerField()
    project_create_file = models.FileField(upload_to='projectcreate/' , blank=True , null=True)
    c_pts = models.IntegerField()
    b_pts = models.IntegerField()
    total = models.IntegerField()
    parent = models.ForeignKey(Parent, on_delete = models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True , blank=True , null=True)
    deadline = models.DateField(blank=True , null=True)
    team = models.ForeignKey(Team, on_delete = models.CASCADE, null =True)
    checksum = models.IntegerField(default = 0)
    available_points = models.IntegerField(default = 0)


class Submission(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    file_project = models.FileField(upload_to = 'files/', null = True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    testing_timestamp = models.DateTimeField(null=True, blank=True)
    after_deadline = models.BooleanField(default=False, editable=True)
    status = models.BooleanField(default=False , editable=True)

from Auction.models import Task
class Points(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
