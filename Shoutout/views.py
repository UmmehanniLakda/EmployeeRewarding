from django.shortcuts import render
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from Client.models import Project , Child , Parent , Team , Emp , Organization , User
from Shoutout.models import Shoutout , Comment
import datetime
from Organization.urls import org_login
from Candidate.urls import emp_login
# Create your views here.

def shoutout_create(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        organization = Organization.objects.get_or_create(user= user)
        employee = Emp.objects.get(user = user)
        employees = Emp.objects.filter(organization=employee.organization.id)
        context['user_name'] = employee.name
        employee_list = []
        print(employee.organization.id)
        for employee in employees.all():
            employee_list.append(employee)
        context['employees'] = employee_list
        shoutouts = Shoutout.objects.all().order_by('-timestamp')
        print(shoutouts)
        shoutout_list = []
        if shoutouts:
            for shoutout in shoutouts:
                comment_list = []
                print(shoutout.emp_appreciated)
                shoutout_list.append(shoutout)
                comments = Comment.objects.filter(shoutout = shoutout)
                for comment in comments.all():
                    comment_list.append(comment)
                context['comments'] = comment_list
                print(comments)
            context['shoutouts'] = shoutout_list
            print('comment',comment_list)
        print(shoutout_list,user)
        if request.method =="POST":
            employee_name = request.POST['employee_name']
            print(employee_name)
            employee_appreciated = Emp.objects.get(id = employee_name , organization=employee.organization)
            description = request.POST['description']
            timestamp = datetime.datetime.now()
            points = request.POST['points']
            print('points:',points)
            if points != '0':
                if int(points) <= employee.points:
                    employee.points -= int(points)
                    employee_appreciated.points += int(points)
                    print(employee_appreciated.points ,employee.points)
                    employee.save()
                    employee_appreciated.save()
                else:
                    context['messages'] = 'You do not have sufficient points'
            Shoutout.objects.create(emp_appreciated=employee_appreciated , emp_appreciator=user ,description=description , timestamp=timestamp)
            print('Shoutout created')
            return HttpResponseRedirect(reverse('shoutout_create'))
    else:
        return HttpResponseRedirect(reverse('emp_login'))
    return render(request , 'shoutouts/shoutout.html' , context)

def shoutout_comment(request,spk):
    context = {}
    shoutout = Shoutout.objects.get(id = spk)
    user = request.user
    context['shoutouts'] = shoutout
    print(shoutout.emp_appreciator)
    comments = Comment.objects.filter(shoutout=shoutout.id).order_by('-timestamp')
    comment_list=[]
    for comment in comments.all():
        comment_list.append(comment)
    context['comments'] = comment_list
    if request.method == "POST":
        comment = request.POST['comment']
        print(shoutout)
        Comment.objects.create(comment=comment , shoutout=shoutout , emp_commented= user , timestamp=datetime.datetime.now())
        print('commented')
        return HttpResponseRedirect(reverse('shoutout_comment' , args=[str(spk)]))
    return render(request , 'shoutouts/shoutout_details.html' , context)

def shoutout_like(request , spk):
    shoutout = Shoutout.objects.get(id = spk)
    user = request.user
    if user.is_active:
        if user in shoutout.likes.all():
            shoutout.likes.remove(user)
        else:
            shoutout.likes.add(user)
        return HttpResponseRedirect(reverse('shoutout_create'))

def comment_like(request , cpk , spk):
    comment = Comment.objects.get(id = cpk)
    user = request.user
    if user.is_active:
        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
    return HttpResponseRedirect(reverse('shoutout_comment' , args=[str(spk)]))
   