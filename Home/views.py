from django.shortcuts import render , reverse
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    return render(request , 'home.html')