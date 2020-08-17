from app_book.models import Sale, Book, Author
from .serializers import BookListSerializer, AuthorSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import mixins, viewsets
from datetime import date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django_filters.rest_framework import DjangoFilterBackend
import unicodecsv


class BookListView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet
                   ):
    serializer_class = BookListSerializer
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('name', 'article_number', 'author__first_name')

    def list(self, request):
        # Dictionary for sorting
        order_by_dict = {'book_name': 'name', 'author_name': 'author__first_name', 'article_number': 'article_number'}
        try:
            books = self.queryset.order_by(order_by_dict[request.GET['order_by']])
        except KeyError:
            books = self.queryset
        paginator = Paginator(books, 20)
        page = self.request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = BookListSerializer(data=request.data)  # read_only=True
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
def AmountView(request):
    """ Return amount of sold books"""
    amount = Sale.objects.all().count()
    return Response({"amount": amount}, status=200)


@api_view(['GET'])
def CurrentYearView(request):
    """ Returns monthly sold books of current year"""
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
    """ Returns sales of previous month"""
    last_month = date.today().month - 1
    sold_books = Sale.objects.filter(date__month=last_month).count()
    return Response({last_month: sold_books}, status=200)


def CSVBooksView(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Type'] = 'application/x-download';
    response['Content-Disposition'] = 'attachment; filename="Books.csv"'
    writer = unicodecsv.writer(response, delimiter=';', encoding='utf-8-sig')
    writer.writerow(['Название', 'Артикул', 'Автор'])
    for book in Book.objects.all():
        writer.writerow([book.name, book.article_number, f'{book.author.first_name} '
                                                         f'{book.author.middle_name} '
                                                         f'{book.author.last_name}'])
    return response


class AuthorSoldBooksView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    """ For statistics of sold books by authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('first_name', 'last_name', 'middle_name')

    def list(self, request):
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


