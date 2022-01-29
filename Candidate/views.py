from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from Client.models import Emp, Organization, Designation, Parent, Child
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.http import HttpResponseRedirect
from Home.urls import home


# Create your views here.
def emp_create(request):
    context = {}
    context['organizations'] = Organization.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['pass2']
        organization_val = request.POST['organization']
        print(organization_val)
        if len(list(Organization.objects.all().filter(name=organization_val))) > 0:
            organization = Organization.objects.all().filter(name=organization_val)[0]
            dob = request.POST['dob']
            if password != password2:
                context['message'] = "Your Passwords Don't Match. Try Again."
            else:
                if username == '' or email == '' or password == '':
                    context['message'] = "Fields aren't filled properly. Please Try again"
                elif len(list(User.objects.all().filter(username=username))) > 0 or len(list(User.objects.all().filter(email=email))) > 0 :
                    context['message'] = "Organization with that username already exists."
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    employee = Emp.objects.create(name=user.username, user=user, points=0, organization=organization,dob=datetime.strptime(dob , '%Y-%m-%dT%H:%M'))
                    return HttpResponseRedirect(reverse('login'))
        else:
            context['message'] = "Organozation Does not Exist"
    return render(request, 'candidate/emp_create.html', context)

def emp_design(request):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        employee = Emp.objects.get(user=user)
        org = employee.organization
        context['designations'] = org.designation_set.all()
        if request.method == "POST":
            design = request.POST['designation']
            print(design)
            employee.designation = design
            employee.save()
            desig_inst = Designation.objects.get(designation=design, organization=org)
            parent_inst, created = Parent.objects.get_or_create(emp=employee)
            for emp in Emp.objects.all().filter(organization=org):
                design_emp = emp.designation
                if design_emp != '':
                    design_emp_inst = Designation.objects.get(designation=design_emp, organization=org)
                    if design_emp_inst.priority > desig_inst.priority:
                        child_inst, created = Child.objects.get_or_create(emp=emp)
                        child_inst.parent.add(parent_inst)
                        child_inst.save()
                    elif design_emp_inst.priority < desig_inst.priority:
                        parent_now, created = Parent.objects.get_or_create(emp=emp)
                        child_now, created = Child.objects.get_or_create(emp=employee)
                        child_now.parent.add(parent_now)
                        child_now.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        context['valid'] = False
    return render(request, 'candidate/emp_design.html', context)

def emp_login(request):
    user = request.user
    context = {}
    context['valid1'] = True
    if not user.is_active:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user is not None:
                auth.login(request, user)
                emp = Emp.objects.get(user=user)
                if emp.designation == '':
                    return HttpResponseRedirect(reverse('emp_design'))
                return HttpResponseRedirect(reverse('home'))
            else:
                context['valid1'] = False
                print('No Login')
                context['message'] = "Please check your Username / Password and Try Again"
                return HttpResponseRedirect(reverse('emp_login'))
    else:
        context['valid1'] = False
    
    return render(request, 'candidate/emp_login.html', context)

def emp_child_list(request):
    context = {}
    user = request.user
    context['valid'] = True
    if user.is_active:
        employee = Emp.objects.get(user=user)
        child_em = []
        try:
            parent = Parent.objects.get(emp=employee)
            children = list(parent.child_set.all())
            for child in children:
                child_em.append(child.emp)
        except:
            pass
        design_text = employee.designation
        org = employee.organization
        design_instance = Designation.objects.get(designation=design_text, organization=org)
        priority = design_instance.priority
        under = Designation.objects.all().filter(priority__gt=priority, organization=org) 
        print(under)
        employees = []
        for design in under:
            for e in list(Emp.objects.all().filter(designation=design.designation)):
                if e not in child_em:
                    employees.append(e)
        con_emp = []
        if request.method == "POST":
            term = request.POST['filter']
            for emp in employees:
                if term.lower() in emp.name.lower() or term.lower() in emp.user.email.lower():
                    con_emp.append(emp)
        else:
            con_emp = employees
        context['employees'] = con_emp
    else:
        context['valid'] = False
    return render(request, 'candidate/emp_setchild.html', context)

def emp_setchild(request, pk):
    user = request.user
    emp = Emp.objects.get(user=user)
    if user.is_active:
        selected = User.objects.get(id=pk)
        selected_emp = Emp.objects.get(user=selected)
        parent_inst, created = Parent.objects.get_or_create(emp=emp)
        child, ucreated = Child.objects.get_or_create(emp=selected_emp)
        child.parent.add(parent_inst)
        return HttpResponseRedirect(reverse('emp_child_list'))
    return render(request, 'candidate/emp_setchild.html')

