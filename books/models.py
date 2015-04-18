from django.db import models

# Create your models here.
class Administrator(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    login_date = models.DateTimeField('last login time')

class Category(models.Model):
    name = models.CharField(max_length=60)

class Author(models.Model):
    name = models.CharField(max_length=20)

class PublishCompany(models.Model):
    name = models.CharField(max_length=60)

class Books(models.Model):
    id = models.CharField(max_length=60, primary_key=True)
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=60)
    pub_com = models.ForeignKey(PublishCompany)
    pub_year = models.CharField(max_length=5)
    author = models.ForeignKey(Author)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    left = models.IntegerField()

class Card(models.Model):
    ower_name = models.CharField(max_length=20)
    borrow_books = models.ManyToManyField(Books)
    limit = models.IntegerField(default=4)
