from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse

from .models import Books

# Create your views here.
def index(request):
    return render(request, 'books/index.html', {})

def search(request):
    book = Books.objects.get(name=request.POST['content']
    
	return HttpResponse('hello')
