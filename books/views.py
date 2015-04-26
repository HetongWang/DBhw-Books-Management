from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login as djangoLogin, logout as djangoLogout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils import timezone

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

    def getCardType(name):
        try:
            p = models.CardType.objects.get(name=name)
        except:
            p = models.CardType.objects.create(name=name)
        return p

    context = RequestContext(request)
    if request.method == 'GET':
        if len(request.GET) == 0:
            return render(request, 'books/libadmin.html', context)
    elif request.post == 'POST':
        data = request.POST

        if data['action'] == 'add_book':
            newbook = models.Books.objects.create(
                pub_com = getPublishCompany(data['pub_com']),
                book_id = data['book_id'],
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
            newcard = models.Card.objects.create(
                card_id = data['card_id'],
                limit = data['limit'],
                fare = data['fare'],
                card_type = getCardType(data['card_type'])
            )
            if newcard is not None:
                newcard.save()

        if data['action'] == 'borrow_book':
            try:
                book = models.Books.objects.get(book_id=data['book'])
                card = models.Card.objects.get(card_id=data['card'])
                if (book.left > 0):
                    book.left -= 1
                    book.save()
                    record = models.Record.objects.create(
                        book = book,
                        card = card,
                        admin = request.user.username
                    )
                    record.save()
                    context.push({'msg': 'borrowed successfully'})
                else:
                    context.push({'msg': 'No book left'})
            except:
                context.push({'msg': 'invalid book id'})
            
        if data['action'] == 'return_book':
            try:
                book = models.Books.objects.get(book_id=data['book'])
                card = models.Card.objects.get(card_id=data['card'])
                record = models.Record.objects.get(book=book, card=card, return_time = None)[0]
                if record is not None:
                    record.return_time = timezone.now()
                    record.save()
                    book.left += 1
                    book.save()
                else:
                    context.push({'msg': 'No record matched'})
            except:
                context.push({'msg': 'No record marched'})
        if data['action'] == 'delete_card':
            try:
                card = models.Card.objects.get(card_id=data['card'])
                record = models.Record.objects.get(card=card, return_time =None)
                if record is None:
                    Card.delete()
                else:
                    context.push({'msg':'This card holder has not returned all the books'})

            except:
                context.push({'msg':'No card matched'})
        if data['action'] == 'delete_book':
            try：
                book = models.Books.objects.get(book_id=data['book'])
                record = models.Record.objects.get(card=card, return_time =None)
                if record is None:
                    Books.delete()
                else:
                    context.push({'msg':'You cannot remove the book from the library, for there are copies remain un-returned'})
            except:
                context.push({'msg':'No book matched'})




