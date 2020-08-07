from django.urls import path
from django.contrib.auth import views
from .views import SignupView, ProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='Signup'),
    path('profile/', ProfileView, name="Profile"),
]