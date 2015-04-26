from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login as djangoLogin, logout as djangoLogout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from . import models
# Create your views here.
def index(request):
    context = RequestContext(request)
    return render(request, 'books/index.html', context)

def search(request, content):
    context = RequestContext(request)
    try:
        context['books'] = models.Books.objects.get(name=content)
    except:
        context['none'] = True
    return render(request, 'books/search.html', context)

def login(request):
    return render(request, 'books/login.html', {})

def logout(request):
    if request.user.is_authenticated():
        djangoLogout(request)
    return HttpResponseRedirect(reverse('books:index'))

def loginConfirm(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        djangoLogin(request, user)
        return HttpResponseRedirect(reverse('books:index'))
    else:
        return render(request, 'books/login.html', {'msg': 'invalid username or password'})

@login_required(login_url='login/')
def libadmin(request):
    
    def getPublishCompany(name):
        try:
            p = models.PublishCompany.objects.get(name=name)
        except:
            p = models.PublishCompany.objects.create(name=name)
        return p

    def getAuthor(name):
        try:
            p = models.Author.objects.get(name=name)
        except:
            p = models.Author.objects.create(name=name)
        return p

    if request.method == 'GET':
        if len(request.GET) == 0:
            context = RequestContext(request)
            return render(request, 'books/libadmin.html', {})
    elif request.post == 'POST':
        data = request.POST
        if data['action'] == 'add_book':
            newbook = Model.Books.objects.create(
                pub_com = getPublishCompany(data['pub_com']),
                id = data['id'],
                name = data['name'],
                pub_year = data['pub_year'],
                price = data['price'],
                amount = data['amount'],
                left = data['amount'],
                category = data['category'],
                author = getAuthor(data['author'])
            )
            if newbook is not None:
                newbook.save()
        if data['action'] == 'add_card':
            newcard = Model.Card.objects.create(
                card_id = data['card_id'],
                limit = data['limit'],
                
                    )

