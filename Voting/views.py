from django.shortcuts import render
from django.contrib.auth.models import User
from Client.models import Emp, Child, Project, Team
from .models import Voting, Votechecksum

# Create your views here.

def teams_all(request):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        emp = Emp.objects.get(user=user)
        child = Child.objects.get(emp=emp)
        teams = child.team_set.all()
        completed_teams = []
        for team in teams:
            project = Project.objects.get(team=team)
            if project.status == True:
                completed_teams.append(team)
        context['teams'] = completed_teams
    else:
        context['valid'] = False
    return render(request, 'voting/team_list.html', context)

def team_vote(request, pk):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        team = Team.objects.get(id=pk)
        children = team.child.all()
        emp = Emp.objects.get(user=user)
        employees = []
        for child in children:
            if child.emp != emp:
                employees.append(child.emp)
        context['employees'] = employees
        context['max_rank'] = [x for x in range(1, len(employees) + 1)]
        if request.method == "POST":
            max_length = len(employees)
            for i in range(1, max_length + 1):
                name = "rank" + str(i)
                rank = request.POST[name]
                user = User.objects.get(username=rank)
                emp_obj = Emp.objects.get(user=user)
                vote_obj, create = Voting.objects.get_or_create(team=team, employee=emp_obj)
                vote_obj.rank += i
                vote_obj.save()
            checksum_obj, created = Votechecksum.objects.get_or_create(team=team)
            checksum_obj.checksum += 1
            checksum_obj.save()
            if checksum_obj.checksum == (max_length + 1):
                minimal = Voting.objects.all().filter(team=team).order_by('rank')[0]
                min_emp = minimal.employee
                project = Project.objects.get(emp=min_emp)
                min_emp.points += project.c_pts
                min_emp.points += project.b_pts
                min_emp.save()
                project.c_pts = 0
                project.b_pts = 0
                project.save()
    else:
        context['valid'] = False
    return render(request, 'voting/team_vote.html', context)
