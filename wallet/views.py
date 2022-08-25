from wallet.models import Wallet
from wallet.serializers import FullWalletSerializer
from rest_framework import viewsets
from rest_framework.permissions import DjangoObjectPermissions, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from django.contrib.auth.models import User


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = FullWalletSerializer
    permission_classes = [DjangoModelPermissions, IsAuthenticatedOrReadOnly]

    # def create(self, request, *args, **kwargs):

    #     response = super().create(request, *args, **kwargs)
    #     return response
