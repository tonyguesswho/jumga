
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.utils import IntegrityError
from rest_framework.generics import (RetrieveUpdateAPIView, ListAPIView)
from api.utils.permissions import IsOwner
from api.serializers.seller import SellerSerializer
from apps.seller.models import Seller
from api.utils.request import RavePayment
from faker import Faker
from django.db import transaction
from apps.delivery.models import Rider
from apps.user.models import Account
import random

import uuid
import os

faker = Faker()


class SellerView(APIView):
    """
    Create seller account
    """
    serializer_class = SellerSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Receives payload to create a seller
        """
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=user)
            except IntegrityError:
                return Response(
                    {"message": "Mulitple stores not allowed yet"}, status=status.HTTP_400_BAD_REQUEST)
            user.is_seller = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerDetailView(RetrieveUpdateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (IsOwner,)
    lookup_field = 'url'
    lookup_url_kwarg = 'seller_id'


class StoreListView(ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerPaymentView(APIView):
    """
    An API view for seller payment
    """
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        """
        Receives payload to send payment request
        """
        user = request.user
        if user.seller.is_active:
            return Response({'message': 'Payment already made'},
                            status=status.HTTP_400_BAD_REQUEST)
        reference = str(uuid.uuid4())
        payload = {
            "amount": settings.SELLER_REG_AMOUNT,
            "currency": settings.JUMGA_DEFAULT_CURRENCY,
            "tx_ref": reference,
            "redirect_url": os.getenv("REDIRECT_URL", '/seller/payment-confirm'),
            "meta": {
                "user_id": user.id,
                "store_name": user.seller.name,
                "store_url": user.seller.url
            },
            "customer": {
                "name": f'{user.first_name} {user.last_name}',
                "email": user.email
            },
            "customizations": {
                "title": "Store Payment",
                #
                "logo": os.getenv("JUMGA_LOGO", "https://res.cloudinary.com/drmmqcxkc/image/upload/v1609630213/JUMGA.png")
            }
        }
        try:
            res = RavePayment().pay(payload=payload)
            return Response(res, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'An error occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentConfirmView(APIView):
    """
    Confirms payment
    """
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        """
        Verify payment using transaction id
        """
        try:
            user = request.user
            seller = user.seller
            res = RavePayment().verify(transaction_id=kwargs.get('transaction_id'))
            result = res['data']
            if (result.get('status') == 'successful') and (result.get('tx_ref') == kwargs.get('trx_ref')):
                if(int(result.get('amount')) < int(settings.SELLER_REG_AMOUNT)) or\
                        (result.get('currency') != settings.JUMGA_DEFAULT_CURRENCY):
                    return Response({'message': 'Wrong amount or currency'},
                                    status=status.HTTP_400_BAD_REQUEST)

                # assign a rider
                riders = list(Rider.objects.all())
                rider = random.choice(riders)
                seller.rider = rider

                # Activate seller
                seller.is_active = True
                seller.save()

                return Response({'message': 'Payment verified', "details": res}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Payment not verified', "details": res}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
