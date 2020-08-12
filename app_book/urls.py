from django.urls import path, include


urlpatterns = [
    path('api/bookshop/', include('app_book.api.urls')),
]