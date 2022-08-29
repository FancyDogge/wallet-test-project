from django.contrib.auth.models import User
from rest_framework.viewsets import mixins, GenericViewSet
from main.serializers import RegistrationSerializer


class RegistrationViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
