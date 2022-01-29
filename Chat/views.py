from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from .models import Message
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponseRedirect
from Client.models import Emp

# Create your views here.
def message_list(request, pk):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        context['pk'] = pk
        context['user'] = user
        rec = User.objects.get(id=pk)
        context['receiver'] = rec
        if request.method == "POST":
            content = request.POST['content']
            Message.objects.create(sender=user, receiver=rec, context=content)
    else:
        context['valid'] = False
    return render(request, 'chat/messages.html', context)

def messages_api(request, pk):
    user = request.user
    data = []
    r_user = User.objects.get(id=pk)
    messages = Message.objects.all().filter(Q(sender=user, receiver=r_user) | Q(sender=r_user, receiver=user)).order_by('timestamp')
    for message in messages:
        if message.sender == user:
            data.append({'user1': message.context})
        elif message.sender == r_user:
            data.append({'user2': message.context})
    return JsonResponse(data, safe=False)

def contacts_list(request):
    user = request.user
    context = {}
    context['valid'] = True
    if user.is_active:
        employee = Emp.objects.get(user=user)
        contacts = Emp.objects.all().filter(organization=employee.organization)
        context['contacts'] = contacts
    else:
        context['valid'] = False
    return render(request, 'chat/messages_list.html', context)
