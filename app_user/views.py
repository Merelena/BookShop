from rest_framework import views, response, permissions, status
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import MyTokenObtainPairSerializer, CustomUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView


class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        content = {
            'first_name': request.first_name.decode('utf-8'),  # `django.contrib.auth.User` instance.
            'last_name': request.last_name.decode('utf-8'),  # None
        }
        return Response(content)

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data={'first_name': request.data})
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
    permission_classes=[IsOwnerProfileOrReadOnly, IsAuthenticated]

