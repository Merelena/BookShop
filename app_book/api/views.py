from app_book.models  import Sale, Book
from .serializers import BookListSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import generics


class BookListView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet
                  ):
    serializer_class = BookListSerializer
    queryset = Book.objects.all()

    def list(self, request):
        serializer = BookListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = BookListSerializer(data=request.data)  # read_only=True
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
def AmountView(request):
    amount = Sale.objects.all().count()
    return Response({"amount": amount}, status=200)
