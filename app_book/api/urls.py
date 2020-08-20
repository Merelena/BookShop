from django.urls import path
from .views import AmountView, BookListView, CurrentYearView, LastMonthView, AuthorSoldBooksView, CSVBooksView, \
    SystemNotificationView, CustomNoficationView, CreateNotificationReadView


urlpatterns = [
    path('amount/', AmountView),
    path('book_list/', BookListView.as_view({'get': 'list', 'post': 'create'})),
    path('current_year/', CurrentYearView),
    path('last_month/', LastMonthView),
    path('authors/', AuthorSoldBooksView.as_view({'get': 'list'})),
    path('system_notice/', SystemNotificationView),
    path('custom_notice/', CustomNoficationView),
    path('new_read_notice/', CreateNotificationReadView.as_view({'post': 'create'})),
    path('', CSVBooksView)
]