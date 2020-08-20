from rest_framework import serializers
from app_book.models import Book, Author, Notification, NotificationRead, Sale
from django.http import HttpResponse


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'article_number', 'author')

    author = AuthorSerializer()


    def create(self, validated_data):
        first_name = validated_data['author']['first_name']
        last_name = validated_data['author']['last_name']
        middle_name = validated_data['author']['middle_name']
        if not Author.objects.filter(first_name=first_name, last_name=last_name, middle_name=middle_name):
            return HttpResponse('Author is not found')
        else:
            instance = Author.objects.get(first_name=first_name, last_name=last_name, middle_name=middle_name)
            validated_data['author'] = instance
            return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        return instance


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'author')

    author = AuthorSerializer()


class NotificationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationRead
        fields = '__all__'


class NotificationSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('message', 'date', 'users', 'is_personal')


class AuthorSoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'middle_name', 'percent')

    percent = serializers.SerializerMethodField()

    def get_percent(self, obj):
        sold_books = Sale.objects.filter(article_number__author=obj).count()
        all_books = Book.objects.filter(author=obj).count()
        percent = 100 * sold_books / all_books
        return percent
