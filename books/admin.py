from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Books, Card, Author, PublishCompany, Administrator, Record

class AdminInline(admin.StackedInline):
    model = Administrator
    can_delete = False
    fields = ['user']

class UserAdmin(admin.ModelAdmin):
    inlines = [AdminInline]
    fieldsets = [
        (None, {'fields': ['username', 'password', 'email']}),
    ]

admin.site.register(Books)
admin.site.register(Card)
admin.site.register(Author)
admin.site.register(PublishCompany)
admin.site.register(Record)
