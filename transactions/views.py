from django.db.models import Q
from rest_framework.viewsets import mixins, GenericViewSet
from transactions.serializers import TransactionSerializer
from transactions.models import Transaction
from rest_framework.permissions import IsAuthenticated

from wallet.models import Wallet

# custom viewset with no PUT, PATCH and DELETE methods
class TransactionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    # getting all transactions where current user wallets are senders OR receivers
    def get_queryset(self):
        transactions = Transaction.objects.all()
        user_wallets = Wallet.objects.filter(owner=self.request.user)
        q = transactions.filter(
            Q(receiver__in=user_wallets) | Q(sender__in=user_wallets)
        )
        return q
