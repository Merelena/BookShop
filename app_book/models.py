from django.db import models
from datetime import date
from app_user.models import CustomUser


class Book(models.Model):
    class Meta:
        ordering = ['article_number']
        verbose_name_plural = 'Книги'
        verbose_name = 'Книга'

    article_number = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)


class Author(models.Model):
    class Meta:
        verbose_name_plural = 'Авторы'
        verbose_name = 'Автор'
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)


class Sale(models.Model):
    class Meta:
        verbose_name_plural = 'Проданные книги'
        verbose_name = 'Проданная книга'

    article_number = models.ForeignKey('Book', on_delete=models.CASCADE)
    date = models.DateField(default=date.today())


class NotificationRead(models.Model):
    users = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notes = models.ForeignKey("Notification", on_delete=models.CASCADE)


class Notification(models.Model):
    message = models.TextField(blank=True, null=True)
    date = models.DateField(default=date.today())
    is_personal = models.BooleanField(default=False, blank=True)
    users = models.ManyToManyField(CustomUser, through=NotificationRead)

    def __str__(self):
        return self.message