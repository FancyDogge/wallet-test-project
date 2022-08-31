from wallet.models import Wallet
from wallet.serializers import FullWalletSerializer
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.permissions import BasePermission


#custom permission, only owner can see his wallets by pk
class IsAuthenticatedAndOwner(BasePermission):
    message = 'You must be the owner of this object.'
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

#custom permission, only sender and receiver can see their transactions by pk
# class IsAuthenticatedAndOwner(BasePermission):
#     message = 'You must be sender or receiver of this transaction.'
#     def has_object_permission(self, request, view, obj):

#         return obj.


# custom viewset with no PUT and PATCH methods
class WalletViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Wallet.objects.all()
    serializer_class = FullWalletSerializer
    permission_classes = [IsAuthenticatedAndOwner]

    # Overriding method of getting queryset to display (only current user wallets)
    def get_queryset(self):
        owner = self.request.user
        return Wallet.objects.filter(owner=owner)
