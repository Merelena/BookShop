from django.urls import path
from .views import AmountView, BookListView, CurrentYearView, LastMonthView, AuthorSoldBooksView, CSVBooksView


urlpatterns = [
    path('amount/', AmountView),
    path('book_list/', BookListView.as_view({'get': 'list', 'post': 'create'})),
    path('current_year/', CurrentYearView),
    path('last_month/', LastMonthView),
    path('authors/', AuthorSoldBooksView.as_view({'get': 'list'})),
    path('', CSVBooksView)
]