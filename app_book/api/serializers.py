from rest_framework import serializers
from app_book.models import Book, Author


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
            instance = Author.objects.create()
            instance.first_name = first_name
            instance.last_name = last_name
            instance.middle_name = middle_name
            instance.save()
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

