from app_book.models import Sale, Book, Author
from .serializers import BookListSerializer, AuthorSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import mixins, viewsets
from datetime import date
from django_filters.rest_framework import DjangoFilterBackend


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


@api_view(['GET'])
def CurrentYearView(request):
    date_now = date.today()
    month = 1
    sold_books = {}
    while month <= date_now.month:
        sold_books[month] = Sale.objects.filter(date__year=date_now.year,
                                                date__month=month).count()
        month += 1
    return Response(sold_books, status=200)


@api_view(['GET'])
def LastMonthView(request):
    last_month = date.today().month - 1
    sold_books = Sale.objects.filter(date__month=last_month).count()
    return Response({last_month: sold_books}, status=200)


class AuthorSoldBooksView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_class = AuthorFilter
    filterset_fields = ('first_name', 'last_name', 'middle_name')
    """filterset_fields = {
        'first_name': ['icontains'],
        'last_name': ['icontains'],
        'middle_name': ['icontains']}"""

    def list(self, request):
        """sold_author_books = []
        author_books = Book.objects.filter(author__first_name__icontains=request.GET['first_name'],
                                           author__last_name__icontains=request.GET['last_name'],
                                           author__middle_name__icontains=request.GET['middle_name']).values('article_number')
        for article_number in author_books:
            if article_number in Sale.objects.values('article_number'):
                temp = Book.objects.get(article_number=article_number['article_number'])
                sold_author_books.append(temp)
        serializer = BookSerializer(sold_author_books, many=True)
        return Response(serializer.data)"""
        sold_books_percent = {}
        first_name = request.GET['first_name']
        last_name = request.GET['last_name']
        middle_name = request.GET['middle_name']
        authors = Author.objects.filter(first_name__icontains=first_name,
                                        last_name__icontains=last_name,
                                        middle_name__icontains=middle_name)
        for author in authors:
            sold_books = Sale.objects.filter(article_number__author=author).count()
            all_books = Book.objects.filter(author=author).count()
            sold_books_percent[f'{author.first_name} {author.middle_name} {author.last_name}'] = \
                100 * sold_books / all_books
        return Response(sold_books_percent)


