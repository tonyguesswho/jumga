

from apps.order.models import Cart, Line, Order
from apps.user.models import Account
from apps.seller.models import Seller
from apps.product.models import Product
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.order import CartSerilaizer, ProductCartSerializer, OrderSerilaizer
from django.shortcuts import get_object_or_404
from decimal import Decimal as D
import uuid
from django.conf import settings
from api.utils.request import RavePayment
import os


class CartView(viewsets.ModelViewSet):
    serializer_class = CartSerilaizer
    queryset = Cart.objects.all()


class ProductCartView(APIView):
    """
    Add product to cart
    """
    serializer_class = ProductCartSerializer

    def post(self, request, *args, **kwargs):
        """
        Receives payload to add to cart
        """
        dt = request.data
        serializer = self.serializer_class(data=dt)
        if serializer.is_valid():
            cart = get_object_or_404(Cart, pk=dt['cart_id'])
            product = get_object_or_404(Product, pk=dt['product_id'])
            cart.add_product(
                product=product, price=product.price)
            return Response({"message": "product added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """
        patch/delete line form cart
        """
        dt = request.data
        serializer = self.serializer_class(data=dt)
        if serializer.is_valid():
            line = get_object_or_404(
                Line, cart_id=dt['cart_id'], product_id=dt['product_id'])
            line.delete()
            return Response({"message": "line deleted"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderPaymentView(APIView):
    """
    Initiate order payment
    """
    serializer_class = OrderSerilaizer

    def post(self, request, *args, **kwargs):
        """
        Receives payload to initiate order placement
        """
        dt = request.data
        lines = Line.objects.filter(cart_id=dt['cart'])
        lines = list(lines)
        price = D(0.00)
        if len(lines) < 1:
            return Response({"message": "No product in cart"}, status=status.HTTP_400_BAD_REQUEST)
        for line in lines:
            price = line.price + price
        order_data = {
            "cart": dt['cart'],
            "seller": dt['seller'],
            "guest_email": dt["email"],
            "status": "awaiting",
            "total_price": price
        }
        seller = get_object_or_404(Seller, pk=dt['seller'])
        rider = seller.rider
        account_details = Account.objects.get(user=seller.user)
        jumga_amount = D(settings.JUMGA_COMM) * price
        serializer = self.serializer_class(data=order_data)
        if serializer.is_valid():
            order = serializer.save()
            shipping_price = order.shipping_price
            jumga_shipping_amount = D(
                settings.JUMGA_COMM_SHIPPING) * (shipping_price)
            reference = str(uuid.uuid4())
            payload = {
                "amount": str(price+shipping_price),
                "currency": settings.JUMGA_DEFAULT_CURRENCY,
                "tx_ref": reference,
                "redirect_url": os.getenv("REDIRECT_URL_ORDER"),
                "meta": {
                    "seller_id": dt['seller'],
                    "email": dt.get('email'),
                    "cart": dt.get("cart"),
                    "order": order.id
                },
                "subacccount": [
                    {
                        "id": account_details.subaccount_id,
                        "transaction_charge_type": "flat_subaccount",
                        "transaction_charge": str(price-jumga_amount)
                    },
                    {
                        "id": rider.subaccount_id,
                        "transaction_charge_type": "flat_subaccount",
                        "transaction_charge": str(shipping_price-jumga_shipping_amount)
                    }
                ],
                "customizations": {
                    "title": "Order Payment",
                },
                "customer": {
                    "cart": dt.get("cart"),
                    "email": dt.get('email')
                }
            }
            try:
                res = RavePayment().pay(payload=payload)
                return Response(res, status=status.HTTP_200_OK)
            except Exception:
                return Response({'message': 'An error occured'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderConfirmView(APIView):
    """
    Confirms order payment
    """

    def get(self, request, *args, **kwargs):
        """
        Verify order payment using transaction id
        """
        try:
            res = RavePayment().verify(transaction_id=kwargs.get('transaction_id'))
            result = res['data']
            order_id = result['meta']['order']
            order = get_object_or_404(Order, pk=order_id)
            if (result.get('status') == 'successful') and (result.get('tx_ref') == kwargs.get('trx_ref')):
                if(int(result.get('amount')) < int(order.total_price)) or\
                        (result.get('currency') != settings.JUMGA_DEFAULT_CURRENCY):
                    return Response({'message': 'Wrong amount or currency'},
                                    status=status.HTTP_400_BAD_REQUEST)

                return Response({'message': 'Payment verified', "details": res}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Payment not verified', "details": res}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
