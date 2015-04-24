from django.contrib import admin

# Register your models here.
from .models import Books, Card, Author, PublishCompany, Administrator

admin.site.register(Books)
admin.site.register(Card)
admin.site.register(Author)
admin.site.register(PublishCompany)
admin.site.register(Administrator)
