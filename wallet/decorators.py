# from wallet.models import Wallet, Transaction
# from rest_framework import serializers
# from functools import wraps

# def make_transaction(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):

#         def get_comission(transfer_amount, bool):
#             return transfer_amount * 0.1 if bool else 0
            
#         #current_user.wallet_set.filter(owner=current_user)
#         try:
#             sender_wallet = self.context["sender"]
#             reciever_wallet = self.context["reciever"] #name=kwargs.validated_data["reciever"]
#             transfer_amount = self.context["transfer_amount"]
#         except: 
#             raise serializers.ValidationError({'error': 'wrong sender or reciever wallet'})

#         # если если валюты в кошельках совпадают, то идем дальше, нет - raise error
#         # если владелец кошелька получателя и сендера совпадает, то комиссия = False else True
#         if sender_wallet.owner == self.context["request"].user:
#             if reciever_wallet.currency == sender_wallet.currency:
#                 if sender_wallet.balance >= transfer_amount:
#                     comission_bool = True if reciever_wallet.owner == sender_wallet.owner else False
#                     transaction = Transaction.objects.create(
#                         sender = sender_wallet,
#                         reciever = reciever_wallet,
#                         transfer_amount = transfer_amount,
#                         comission = get_comission(transfer_amount, comission_bool)
#                     )
                    
#                     return transaction   
#             raise serializers.ValidationError({'error': 'wallet currencies are not matching!'})
#         raise serializers.ValidationError({'error': 'wrong sender wallet'})
#     return wrapper
            
