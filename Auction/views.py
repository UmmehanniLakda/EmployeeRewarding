from django.shortcuts import render, reverse
from datetime import datetime
from .models import Task, Tasksubmissionfile, Taskbid, Taskassigned, Tasksubmission
from Client.models import Emp, Points
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User

# Create your views here.

def create_task(request):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        if request.method == "POST":
            employee = Emp.objects.get(user=user)
            name = request.POST['name']
            description = request.POST['description']
            try:
                file_obj = request.FILES['attachment']
            except:
                file_obj = None
            max_points = request.POST['points']
            deadline = datetime.strptime(request.POST['deadline'] , '%Y-%m-%dT%H:%M')
            if file_obj:
                task = Task.objects.create(name=name, description=description, creator=employee, max_reward=max_points, attachment=file_obj, deadline=deadline)
            else:
                task = Task.objects.create(name=name, description=description, creator=employee, max_reward=max_points, deadline=deadline)
            return HttpResponseRedirect(reverse('task_list'))
    else:
        context['valid'] = False
        context['message'] = "Please login To Continue"
    return render(request, 'auction/create_task.html', context)


def task_list(request):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        tasks = Task.objects.all().filter(assigned=False).filter(deadline__gt=timezone.now()).order_by('-timestamp')
        context['tasks'] = tasks
    else:
        context['valid'] = False
    return render(request, 'auction/task_list.html', context)

def task_detail(request, pk):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        task = Task.objects.get(id=pk)
        task_bids = Taskbid.objects.all().filter(task=task).order_by('bid')
        context['task'] = task
        context['bids'] = task_bids
        employee = Emp.objects.get(user=user)
        print(employee)
        print(task.creator)
        if employee == task.creator:
            context['creator'] = True
        if request.method == "POST":
            bid = int(request.POST['bid'])
            employee = Emp.objects.get(user=user)
            Taskbid.objects.create(task=task, employee=employee, bid=bid)
    else:
        context['valid'] = False
    return render(request, 'auction/task_detail.html', context)

def assign_task(request, tpk, epk):
    user = request.user
    task = Task.objects.get(id=tpk)
    assigned_to = Emp.objects.get(id=epk)
    context = {}
    context['valid'] = True
    if user.is_active:
        task.assigned = True
        task.save()
        task_bid = Taskbid.objects.filter(task=task, employee=assigned_to).order_by('-timestamp')[0]
        bid = task_bid.bid
        Taskassigned.objects.create(task=task, assigned_to=assigned_to, bid_points=bid)
        return HttpResponseRedirect(reverse('task_list'))
    else:
        context['valid'] 
    

def assigned_tasks(request):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        employee = Emp.objects.get(user=user)
        assigned_tasks_incomplete = employee.task_set.all().filter(assigned=True, completed=False).order_by('-timestamp')
        assigned_tasks_complete = employee.task_set.all().filter(assigned=True, completed=True).order_by('-timestamp')
        incomplete = []
        complete = []
        print('Assigned:',assigned_tasks_complete)
        print(assigned_tasks_incomplete)
        for task in assigned_tasks_incomplete:
            incomplete.append((task, task.taskassigned_set.all()))

        for task in assigned_tasks_complete:
            complete.append((task, task.taskassigned_set.all()))
        
        context['incomplete_tasks'] = incomplete
        context['completed_tasks'] = complete
        return render(request, 'auction/assigned_tasks.html', context)
    else:
        context['valid'] = False
    return render(request, 'auction/assigned_tasks.html', context)

def my_assignment(request):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        employee = Emp.objects.get(user=user)
        assigned_tasks = Taskassigned.objects.all().filter(assigned_to=employee)
        completed_tasks = []
        incomplete_tasks = []
        for atask in assigned_tasks:
            if atask.task.completed == True:
                completed_tasks.append((atask.task, atask))
            else:
                incomplete_tasks.append((atask.task, atask))
        context['incomplete_tasks'] = incomplete_tasks
        context['completed_tasks'] = completed_tasks
        print('Incomplete',incomplete_tasks)
        print('complete',completed_tasks)
        return render(request, 'auction/my_tasks.html', context)
    else:
        context['valid'] = False
    return render(request, 'auction/my_tasks.html', context)

def create_submission(request, pk):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        assignment = Taskassigned.objects.get(id=pk)
        task = assignment.task
        context['task'] = task
        employee = Emp.objects.get(user=user)
        assignments = task.taskassigned_set.all()
        allowed = []
        for assign in assignments:
            allowed.append(assign.assigned_to)
        if employee in allowed:
            if request.method == "POST":
                title = request.POST['title']
                description = request.POST['description']
                try:
                    file1 = request.FILES['file1']
                except:
                    file1 = None
                try:
                    file2 = request.FILES['file1']
                except:
                    file2 = None
                try:
                    file3 = request.FILES['file1']
                except:
                    file3 = None
                submission = Tasksubmission.objects.create(assignment=assignment, employee=employee, text=title, description=description)
                for file_inst in [file1, file2, file3]:
                    if file_inst:
                        Tasksubmissionfile.objects.create(submission=submission, file_item=file_inst)
                return HttpResponseRedirect(reverse('my_assignment'))
        else:
            context['valid'] = False
    else:
        context['valid'] = False
    return render(request, 'auction/submission.html', context)

def my_submission_list(request, pk):
    user = request.user
    context = {}
    context['valid'] = True
    context['assigned'] = False
    if user.is_active:
        employee = Emp.objects.get(user=user)
        task_assigned = Taskassigned.objects.get(id=pk)
        if employee == task_assigned.assigned_to:
            context['assigned'] = True
            submission_list = Tasksubmission.objects.all().filter(assignment=task_assigned).order_by('-timestamp')
            context['submissions'] = submission_list
            context['task'] = task_assigned.task
        else:
            context['message'] = "This task is not been assigned to you."
            context['valid'] = False
    else:
        context['valid'] = False
    return render(request, 'auction/my_submission_list.html', context)


def task_submission_list(request, pk):
    user = request.user
    context = {}
    context['valid'] = True
    context['created'] = False
    if user.is_active:
        employee = Emp.objects.get(user=user)
        task_assigned = Taskassigned.objects.get(id=pk)
        if employee == task_assigned.task.creator:
            submission_list = Tasksubmission.objects.all().filter(assignment=task_assigned)
            context['submissions'] = submission_list
            context['task'] = task_assigned.task
        else:
            context['message'] = "This task is not been created to you."
            context['created'] = True
    else:
        context['valid'] = False
    return render(request, 'auction/task_submission_list.html', context)


def submission_accept(request, pk):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        employee = Emp.objects.get(user=user)
        submission = Tasksubmission.objects.get(id=pk)
        creator = submission.assignment.task.creator
        if employee == creator:
            submission_files = submission.tasksubmissionfile_set.all()
            context['submission'] = submission
            if list(submission_files) == []:
                context['files'] = []
            else:
                context['files'] = submission_files
            task = submission.assignment.task
            task_assigned = Taskassigned.objects.get(task = task)
            print(task_assigned)
            context['task'] = task
            print(task.id)
            accepted_val = False
            if request.method == "POST":
                try:
                    accepted = request.POST['accepted']
                    accepted_val = True
                except:
                    accepted_val = False
    
                if accepted_val:
                    submission.accepted = True
                    submission.save()
                    submission.assignment.status = True
                    submission.assignment.save()
                    task.completed = True
                    task.save()
                    creator = task.creator
                    bid_points = submission.assignment.bid_points
                    submitter = submission.employee
                    creator.points -= bid_points
                    creator.save()
                    submitter.points += bid_points
                    submitter.save()
                    creator_user = creator.user
                    submitter_user = submitter.user
                    Points.objects.create(sender=creator_user, reciever=submitter_user, points=bid_points, task=task)
                    return HttpResponseRedirect(reverse('task_submission_list' , args = [int(task_assigned.id)]))
                else:
                    submission.accepted = False
                    submission.save()
                    submission.assignment.status = False
                    submission.assignment.save()
                    task.completed = False
                    task.save()
        else:
            context['message'] = "You are not the creator of this task."
            context['valid'] = False
    else:
        context['valid'] = False
    return render(request, 'auction/submission_accept.html', context)


