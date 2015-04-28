from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Administrator(models.Model):
    user = models.OneToOneField(User)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

class Author(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class PublishCompany(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Books(models.Model):
    book_id = models.CharField(max_length=60, primary_key=True)
    category = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    pub_com = models.ForeignKey(PublishCompany)
    pub_year = models.CharField(max_length=5)
    author = models.ForeignKey(Author)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    amount = models.IntegerField(default=1)
    left = models.IntegerField()

    search = models.TextField(default='')

    def save(self, *args, **kwargs):
        self.search = self.book_id + ' ' + self.name + ' ' + self.category + ' ' + self.pub_com.name + ' ' + self.author.name + ' '
        if self.left is None:
            self.left = self.amount
        super(Books, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class CardType(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Card(models.Model):
    card_id = models.CharField(max_length=20, primary_key=True)
    limit = models.IntegerField(default=4)
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    card_type = models.ForeignKey(CardType)

    def __str__(self):
        return self.card_id

class Record(models.Model):
    book = models.ForeignKey(Books)
    card = models.ForeignKey(Card)
    borrow_time = models.DateTimeField(auto_now_add=True)
    return_time = models.DateTimeField(null=True)
    admin = models.ForeignKey(User)

