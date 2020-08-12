from django.urls import path
from .views import AmountView, BookListView


urlpatterns = [
    path('amount/', AmountView),
    path('book_list/', BookListView.as_view({'get': 'list', 'post': 'create'}))
]