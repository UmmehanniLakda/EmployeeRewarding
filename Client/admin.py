from django.contrib import admin
from . models import Child, Emp, Parent, Project, Team, Organization , Submission, ParentProject, Points
from . models import Child, Emp, Parent, Project, Team, Organization, Submission

# Register your models here.
admin.site.register(Organization)
admin.site.register(Child)
admin.site.register(Emp)
admin.site.register(Parent)
admin.site.register(Project)
admin.site.register(Team)
admin.site.register(Submission)
admin.site.register(ParentProject)
admin.site.register(Points)



