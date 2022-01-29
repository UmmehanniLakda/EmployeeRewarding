from django.shortcuts import render
from Client.models import Points, Emp, Organization, Parent, Team, Project, Child, Submission
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.http import JsonResponse
# Create your views here.


def weekly_lead(request):
    current = timezone.now()
    days = datetime.timedelta(days=7)
    user_points = {}
    user = request.user
    context = {}
    context['valid'] = True
    try:
        organization = Organization.objects.get(user=user)
    except:
        try:
            employee = Emp.objects.get(user=user)
            organization = employee.organization
        except:
            organization = None
    if organization:
        for user in User.objects.all():
            try:
                employee = Emp.objects.get(user=user, organization=organization)
            except:
                employee = None
            if employee:
                if user not in user_points.keys():
                    user_points[user] = 0
        for point in Points.objects.all():
            if point.reciever in user_points.keys():
                if current - point.timestamp < days: 
                    user_points[point.reciever] += point.points
        points_manager = []
        print(user_points)
        for key in user_points.keys():
            emp = Emp.objects.get(user=key)
            points_manager.append((emp, user_points[key]))
        points_manager.sort(key=lambda x: x[1])
        points_manager.reverse()
        context['points_manager'] = points_manager
        context['current'] = current
    else:
        context['valid'] = False
    return render(request, 'leaderboard/weekly_lead.html', context)


def yearly_lead(request):
    current = timezone.now()
    days = datetime.timedelta(days=365)
    user_points = {}
    user = request.user
    context = {}
    context['valid'] = True
    try:
        organization = Organization.objects.get(user=user)
    except:
        try:
            employee = Emp.objects.get(user=user)
            organization = employee.organization
        except:
            organization = None
    if organization:
        for user in User.objects.all():
            try:
                employee = Emp.objects.get(user=user, organization=organization)
            except:
                employee = None
            if employee:
                if user not in user_points.keys():
                    user_points[user] = 0
        for point in Points.objects.all():
            if point.reciever in user_points.keys():
                if current - point.timestamp < days: 
                    user_points[point.reciever] += point.points
        points_manager = []
        for key in user_points.keys():
            emp = Emp.objects.get(user=key)
            points_manager.append((emp, user_points[key]))
        points_manager.sort(key=lambda x: x[1])
        points_manager.reverse()
        context['points_manager'] = points_manager
        context['current'] = current
    else:
        context['valid'] = False
    return render(request, 'leaderboard/yearly_lead.html', context)


def quaterly_lead(request):
    current = timezone.now()
    days = datetime.timedelta(days=90)
    user_points = {}
    user = request.user
    context = {}
    context['valid'] = True
    try:
        organization = Organization.objects.get(user=user)
    except:
        try:
            employee = Emp.objects.get(user=user)
            organization = employee.organization
        except:
            organization = None
    if organization:
        for user in User.objects.all():
            try:
                employee = Emp.objects.get(user=user, organization=organization)
            except:
                employee = None
            if employee:
                if user not in user_points.keys():
                    user_points[user] = 0
        for point in Points.objects.all():
            if point.reciever in user_points.keys():
                if current - point.timestamp < days: 
                    user_points[point.reciever] += point.points
        points_manager = []
        for key in user_points.keys():
            emp = Emp.objects.get(user=key)
            points_manager.append((emp, user_points[key]))
        points_manager.sort(key=lambda x: x[1])
        points_manager.reverse()
        context['points_manager'] = points_manager
        context['current'] = current
    else:
        context['valid'] = False
    return render(request, 'leaderboard/quaterly_lead.html', context)

def points_chart(request):
    return render(request, 'leaderboard/points_chart.html')

def points_chart_data(request):
    user = request.user
    data = []
    if user.is_active:
        try:
            organization = Organization.objects.get(user=user)
            print('organization',organization)
        except:
            try:
                employee = Emp.objects.get(user=user)
                organization = employee.organization
                print('organizzation of employee',organization)
            except:
                organization = None
        print(organization)
        if organization:
            days = datetime.timedelta(days=30)
            current = timezone.now()
            for emp in Emp.objects.all().filter(organization=organization).order_by('-points')[:5]:
                points = Points.objects.filter(reciever=emp.user)
                total = 0
                for point in points:
                    if current - point.timestamp < days:
                        total += point.points
                data.append({emp.user.username: total})
    print(data)
    return JsonResponse(data, safe=False)


def teams_charts_data(request):
    user = request.user
    data = []
    if user.is_active:
        try:
            organization = Organization.objects.get(user=user)
        except:
            try:
                employee = Emp.objects.get(user=user)
                organization = employee.organization
            except:
                organization = None
        if organization:
            teams = Team.objects.all()
            for team in teams:
                try:
                    if team.parent.emp.organization == organization:
                        total = 0
                        projects = Project.objects.filter(team=team, status=True)
                        for project in projects:
                            total += project.total
                        data.append({team.name: total})
                except:
                    try:
                        if team.organization == organization:
                            total = 0
                            projects = Project.objects.filter(team=team, status=True)
                            for project in projects:
                                total += project.total
                            data.append({team.name: total})
                    except:
                        pass
    return JsonResponse(data, safe=False)

def teams_chart(request):
    return render(request, 'leaderboard/teams_chart.html')


def emp_progress(request):
    user = request.user
    data = []
    if user.is_active:
        employee = Emp.objects.get(user=user)
        child = Child.objects.get(emp=employee)
        submissions = Submission.objects.all().filter(child=child, status=True).order_by('-testing_timestamp')
        if len(list(submissions)) > 10:
            submissions = submissions[:10]
        submissions = submissions[::-1]
        data.append({str(employee.doj.date()) + '(Joined)': 0})
        for submission in submissions:
            data.append({str(submission.testing_timestamp.date()) + ' (' + submission.project.name + ')': submission.project.total // len(submission.project.team.child.all())})
    return JsonResponse(data, safe=False)

def emp_progress_chart(request):
    return render(request, 'leaderboard/emp_chart.html')