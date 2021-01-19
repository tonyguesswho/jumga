
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.utils.request import Banks, SubAccount
from api.serializers.account import AccountSerilaizer
from api.utils.permissions import IsSeller
from apps.user.models import Account
from rest_framework.generics import (RetrieveUpdateAPIView)
from api.utils.permissions import IsOwner


class GetBanksView(APIView):
    """
    Confirms payment
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Get bank list
        """
        try:
            res = Banks().get_banks(country=kwargs.get('country'))
            return Response(res, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AccountsView(APIView):
    """
    Create sub account
    """
    serializer_class = AccountSerilaizer
    permission_classes = (IsSeller,)

    def post(self, request, *args, **kwargs):
        """
        Receives payload to create a sub account
        """
        user = request.user
        seller = user.seller
        data = request.data
        account_data = {
            "account_bank": data['bank_code'],
            "account_number": data['account_number'],
            "business_name": seller.name,
            "business_email": user.email,
            "business_mobile": data['mobile'],
            "country": data['country_code'],
            "split_type": "percentage",
            "split_value": 0.97
        }
        try:
            res = SubAccount().create(payload=account_data)
        except Exception:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response_data = res["data"]
        data["subaccount_id"] = response_data['subaccount_id']
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailView(RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerilaizer
    permission_classes = (IsOwner,)
    lookup_field = 'user'
    lookup_url_kwarg = 'user_id'
