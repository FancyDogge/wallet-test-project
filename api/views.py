from api.models import Wallet
from api.serializers import FullWalletSerializer, BasicWalletSerializer
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = FullWalletSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)
        return response
