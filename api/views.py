from api.models import Wallet
from api.serializers import FullWalletSerializer, RegistrationSerializer
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.contrib.auth.models import User


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = FullWalletSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)
        return response


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer