import django_filters
from app_book.models import Author


class AuthorFilter(django_filters.FilterSet):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'middle_name']
    #irst_name = django_filters.CharFilter(lookup_expr='icontains')
    #ast_name = django_filters.CharFilter(lookup_expr='icontains')
    #middle_name = django_filters.CharFilter(lookup_expr='icontains')