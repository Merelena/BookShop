from django.shortcuts import render
from rest_framework.response import Response
from .models import Book
#from .serializers import BookSerializer, OneBookSerializer, BookCreateSerializer
from rest_framework import viewsets
from rest_framework import mixins
#from .filters import BookFilter
#from django_filters.rest_framework import DjangoFilterBackend


class BookView(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               viewsets.GenericViewSet):

    queryset = Book.objects.all()
    #filter_backends = [DjangoFilterBackend]
    #filterset_class = BookFilter



