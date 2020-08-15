from django.db import models
from django.utils import timezone
from datetime import date


class Book(models.Model):
    article_number = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)

    """def __init__(self, first_name, last_name, middle_name):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name"""


class Sale(models.Model):
    article_number = models.ForeignKey('Book', on_delete=models.CASCADE)
    date = models.DateField(default=date.today())