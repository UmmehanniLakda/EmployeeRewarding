from django.shortcuts import render, redirect, reverse
from Client.models import Organization, Submission, Child, Team, Emp, Project, Parent, ParentProject, Points
from django.shortcuts import render                  
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from .models import Designation
from datetime import datetime
from django.utils import timezone
from Candidate.urls import emp_login
from Home.urls import home



# Create your views here.

def org_login(request):
    user = request.user
    context = {}
    context['valid1'] = True
    context['organization'] = True
    if not user.is_active:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user is not None:
                auth.login(request, user)
            else:
                context['message'] = "Please check you Username / Password and Try Again"
            return HttpResponseRedirect(reverse('home'))
    else:
        context['valid1'] = False
    return render(request, 'organization/org_login.html', context)


def org_create(request):
    user = request.user
    context = {}
    context['valid1'] = True
    context['organization'] = True
    if not user.is_active:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['pass2']
            description = request.POST['description']
            if password != password2:
                context['message'] = "Your Passwords Don't Match. Try Again."
            else:
                if username == '' or email == '' or password == '':
                    context['message'] = "Fields aren't filled properly. Please Try again"
                elif len(list(User.objects.all().filter(username=username))) > 0 or len(list(User.objects.all().filter(email=email))) > 0 :
                    context['message'] = "Organization with that username already exists."
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    organization = Organization.objects.create(name=user.username, description=description, user=user)
                return HttpResponseRedirect(reverse('org_login'))
    else:
        context['valid1'] = False
    return render(request, 'organization/org_create.html', context)

def org_architecture(request):
    context = {}
    user = request.user
    organization = Organization.objects.get(user=user) or None
    print(organization.confirmed)
    context['organization'] = True
    if organization.desigset == False:
        context['valid'] = True
        if request.method == "POST":
            organization.desigset = True
            organization.save()
            for i in range(1, 11):
                try:
                    name = 'text-' + str(i)
                    desig = request.POST[name]
                    if desig != '':
                        Designation.objects.create(organization=organization, designation=desig, priority=i)
                except:
                    break
            return HttpResponseRedirect(reverse('home'))
    else:
        if organization is None:
            context['invalid'] = True
        context['valid'] = False
    return render(request, 'organization/org_architecture.html', context)


def team_create(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        employee = Emp.objects.get(user = user)
        parents = Parent.objects.get(emp = employee)
        children = Child.objects.filter(parent = parents)
        context['children'] = children
        print(children)
        if request.method == 'POST':
            team_name = request.POST['team_name']
            name1 = request.POST['name1']
            name2 = request.POST['name2']
            name3 = request.POST['name3']
            name4 = request.POST['name4']
            team = Team.objects.create(name = team_name, parent = parents)
            if name1:
                print(name1)
                emp_in = Emp.objects.get(name=name1)
                child1 = Child.objects.get(emp=emp_in)
                team.child.add(child1)
            if name2:
                emp_in = Emp.objects.get(name=name1)
                child2 = Child.objects.get(emp=emp_in)
                team.child.add(child2)
            if name3:
                emp_in = Emp.objects.get(name=name1)
                child3 = Child.objects.get(emp=emp_in)
                team.child.add(child3)
            if name4:
                emp_in = Emp.objects.get(name=name1)
                child4 = Child.objects.get(emp=emp_in)
                team.child.add(child4)
            return HttpResponseRedirect(reverse('create_project'))
    else:
        return HttpResponseRedirect(reverse('emp_login'))
    return render(request, 'organization/team_create.html', context)


def org_create_project(request):
    user = request.user
    context = {}
    context['valid'] = True
    context['organization'] = True
    if user.is_active:
        try:
            organization = Organization.objects.get(user=user)
        except:
            organization = None
        if organization:
            context['teams'] = Team.objects.all().filter(organization=organization)
            if request.method == "POST":
                name = request.POST['name']
                description = request.POST['description']
                team_name = request.POST['team']
                team = Team.objects.get(name=team_name, organization=organization)
                try:
                    file_instance = request.POST['file']
                except:
                    file_instance = None
                deadline = request.POST['deadline']
                points = request.POST['points']
                c_points = request.POST['c_points']
                b_points = request.POST['b_points']
                parent_project = ParentProject.objects.create(organization=organization, name=name)
                if file_instance:
                    project = Project.objects.create(parentproject = parent_project, name=name, description=description, default_pts=points, project_create_file=file_instance, c_pts=c_points, b_pts=b_points, total=points + c_points + b_points, deadline=datetime.strptime(deadline , '%Y-%m-%dT%H:%M'), team=team)
                else:
                    project = Project.objects.create(parentproject = parent_project, name=name, description=description, default_pts=points, c_pts=c_points, b_pts=b_points, total=int(points) + int(c_points) + int(b_points), deadline=datetime.strptime(deadline , '%Y-%m-%dT%H:%M'), team=team)
                return HttpResponseRedirect(reverse('parent_project_list'))
        else:
            context['valid'] = False
    else:
        context['valid'] = False
    return render(request, 'organization/create_project.html', context)

def org_project_accept(request, pk):
        user = request.user
        context = {}
        context['valid'] = True
        context['organization'] = True
        if user.is_active:
            try:
                organization = Organization.objects.get(user=user)
            except:
                context['valid'] = False
                organization = None
            if organization:
                submission = Submission.objects.get(id=pk)
                creator = submission.project.parentproject.organization
                if organization == creator:
                    if submission.file_project:
                        submission_file = submission.file_project
                    else:
                        submission_file = []
                    context['submission'] = submission
                    context['file'] = submission_file
                    context['project'] = submission.project
                    accepted_val = False
                    if request.method == "POST":
                        try:
                            accepted = request.POST['accepted']
                            accepted_val = True
                        except:
                            accepted_val = False
            
                        if accepted_val:
                            submission.status = True
                            submission.save()
                            submission.project.status = True
                            submission.project.save()
                            creator = submission.project.parentproject.organization
                            submitter = submission.child.emp
                            submitter.points += submission.project.default_pts // 3
                            Points.objects.create(sender=creator.user, reciever=submitter.user, points = submission.project.default_pts // 3, project = submission.project)
                            if submission.project.deadline > timezone.now().date():
                                submission.after_deadline = True
                            submitter.save()
                        else:
                            submission.accepted = False
                            submission.save()
                            submission.project.status = True
                            submission.project.save()
                        return HttpResponseRedirect(reverse('org_submission_list' , args=[str(submission.project.id)]))
                else:
                    context['message'] = "You are not the creator of this project."
                    context['valid'] = False
        else:
            context['valid'] = False
        return render(request, 'organization/submission_accept.html', context)

def org_submission_list(request, pk):
    user = request.user
    context = {}
    context['valid'] = True
    context['organization'] = True
    if user.is_active:
        organization = Organization.objects.get(user=user)
        project = Project.objects.get(id=pk)
        if organization == project.parentproject.organization:
            submission_list = Submission.objects.all().filter(project=project)
            context['submissions'] = submission_list
            context['project'] = project
        else:
            context['message'] = "This Project is not been created to you."
            context['created'] = True
    else:
        context['valid'] = False
    return render(request, 'organization/submission_list.html', context)

# Parent Project List
def parent_project_list(request):
    user = request.user
    context = {}
    context['valid'] = True
    context['organization'] = True
    if user.is_active:
        try:
            organization = Organization.objects.get(user=user)
        except:
            organization = None
        if organization:
            parentprojects = organization.parentproject_set.all()
            context['projects'] = parentprojects
            context['organization'] = organization
        else:
            context['valid'] = False
    else:
        context['valid'] = False
    return render(request, 'organization/parent_list.html', context)


# List of Projects in Parent Project

def org_projects_list(request, pk):
    user = request.user
    context = {}
    context['valid'] = True
    context['notyours'] = False
    context['organization'] = True
    if user.is_active:
        try:
            organization = Organization.objects.get(user=user)
        except:
            organization = None
        if organization:
            parentproject = ParentProject.objects.get(id=pk)
            if parentproject in organization.parentproject_set.all():
                context['projects'] = parentproject.project_set.all()
                context['parent'] = parentproject
                context['organization'] = organization
            else:
                context['notyours'] = True
        else:
            context['valid'] = False
    else:
        context['valid'] = False
    return render(request, 'organization/project_list.html', context)


def org_team_create(request):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        organization = user.organization
        employees = Emp.objects.all().filter(organization=organization)
        context['employees'] = employees
        if request.method == 'POST':
            team_name = request.POST['title']
            team = Team.objects.create(name=team_name, organization=organization)
            for i in range(1, 11):
                try:
                    name = 'member-' + str(i)
                    member = request.POST[name]
                    member_inst = Emp.objects.get(name=member)
                    print(member_inst)
                    child_inst, created = Child.objects.get_or_create(emp=member_inst)
                    team.child.add(child_inst)
                    team.save()
                except:
                    pass
            return HttpResponseRedirect(reverse('org_create_project'))     
    else:
        context['valid'] = False
    return render(request, 'organization/org_team_create.html', context)

def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect(reverse('home'))
            
