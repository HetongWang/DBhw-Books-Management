from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Administrator(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    login_date = models.DateTimeField('last login time')

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class PublishCompany(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Books(models.Model):
    id = models.CharField(max_length=60, primary_key=True)
    category = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    pub_com = models.ForeignKey(PublishCompany)
    pub_year = models.CharField(max_length=5)
    author = models.ForeignKey(Author)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    left = models.IntegerField()

    def __str__(self):
        return self.name

class Card(models.Model):
    user = models.OneToOneField(User)
    card_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=40)
    limit = models.IntegerField(default=4)
    fine = models.DecimalField(max_digits=10, decimal_places=2)

class Record(models.Model):
    book = models.ForeignKey(Books)
    card = models.ForeignKey(Card)
    borrow_time = models.DateTimeField(auto_now_add=True)
    return_time = models.DateTimeField()

