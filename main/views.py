from django.contrib.auth.models import User
from rest_framework import viewsets
from main.serializers import RegistrationSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer