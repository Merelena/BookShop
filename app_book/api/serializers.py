from rest_framework import serializers
from app_book.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def create(self, **validated_data):
        return Author.objects.create(**validated_data)


class BookListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ('name', 'article_number', 'author')

    def create(self, validated_data):
        instance = Author.objects.create()
        instance.first_name = validated_data['author']['first_name']
        instance.last_name = validated_data['author']['last_name']
        instance.middle_name = validated_data['author']['middle_name']
        validated_data['author'] = instance
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        return instance
