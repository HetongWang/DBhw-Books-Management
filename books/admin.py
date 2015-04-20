from django.contrib import admin

# Register your models here.
from .models import Books, Card

admin.site.register(Books)
admin.site.register(Card)   
