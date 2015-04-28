import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate, login as djangoLogin, logout as djangoLogout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils import timezone

from books import models
# Create your views here.


def index(request):
    context = RequestContext(request)
    return render(request, 'books/index.html', context)


def search(request, content):
    context = RequestContext(request)
    try:
        books = models.Books.objects.get(name=content)
        if not (type(books) is list):
            books = [books]
        context.push({'books': books})
    except:
        context.push({'none': True})
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


@login_required(login_url='/login/')
def libadmin(request):
    context = {
        'msg': '',
        'err': False
    }
    
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

    def opError(msg=''):
        context['msg'] = msg
        context['err'] = True


    if request.method == 'GET':
        if len(request.GET) == 0:
            context = RequestContext(request)
            return render(request, 'books/libadmin.html', context)

    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if data['action'] == 'add_book':
            try:
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
                else:
                    opError('Add Book Failed, Please Check if card is conflict')
            except Exception as e:
                opError(str(e))

        if data['action'] == 'add_card':
            try:
                newcard = models.Card.objects.create(
                    card_id = data['card_id'],
                    limit = data['limit'],
                    card_type = getCardType(data['card_type'])
                )
                if newcard is not None:
                    newcard.save()
                else:
                    opError('Add Card Failed, Please Check if card is conflict')
            except Exception as e:
                opError(str(e))

        if data['action'] == 'book_borrow':
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
                else:
                    record = models.Record.objects.get(book=book, card=card, return_time = None).order_by('-borrow_time')[0]
                    msg = 'Nearest Return time' + record.borrow_time
                    opError(msg)
            except:
                opError('Invalid Book Id')
            
        if data['action'] == 'book_return':
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
                    opError('No record matched')
            except:
                opError('No record marched')

        if data['action'] == 'del_card':
            try:
                card = models.Card.objects.get(card_id=data['card'])
                record = models.Record.objects.get(card=card, return_time = None)
                if record is None:
                    card.delete()
                else:
                    opError('This card holder has not returned all the books')
            except:
                opError('No card matched')

        if data['action'] == 'del_book':
            try:
                book = models.Books.objects.get(book_id=data['book_id'])
                try:
                    record = models.Record.objects.get(book=book, return_time=None)
                except:
                    book.delete()
                else:
                    opError('You cannot remove the book from the library, for there are copies remain un-returned')
            except:
                opError('No book matched')

        jsondata = json.dumps(context)
        return HttpResponse(jsondata, content_type="application/json")

