import email
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Publisher(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return (self.name)

class LibraryUser(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)

    def __str__(self):
        return (self.user.first_name + ' ' + self.user.last_name)

class Author(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)
    # first_name = models.CharField(max_length=100, null=True)
    # last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    age = models.IntegerField()

    def __str__(self):
        return (self.user.first_name + ' ' + self.user.last_name)


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, blank=True)
    publisher_date = models.DateField()
    stars = models.DecimalField(default=0, max_digits=3,decimal_places=2,validators=[MinValueValidator(0.01),MaxValueValidator(5)])
    rates = models.IntegerField(default=0)
    book = models.FileField(blank=True)

    def __str__(self):
        return (self.title)