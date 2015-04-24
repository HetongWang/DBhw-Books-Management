from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from .models import Books

# Create your views here.
def index(request):
    context = {
        'is_login': request.user.is_authenticated(),
        'user': request.user
    }
    return render(request, 'books/index.html', context)

def search(request, content):
    context = {
        'books': {},
        'none': False
    }
    try:
        context['books'] = Books.objects.get(name=content)
    except:
        context['none'] = True
    return render(request, 'books/search.html', context)

def login(request):
    return render(request, 'books/login.html', {})

def loginConfirm(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(user)
    else:
        pass

def libadmin(request):
    return render(request, 'books/libadmin.html', {})

