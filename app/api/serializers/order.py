

from rest_framework import serializers
from apps.order.models import Cart, Line, Order
from api.serializers.product import ProductSerilaizer


class LineSerilaizer(serializers.ModelSerializer):
    product = ProductSerilaizer(many=False, read_only=True)

    class Meta:
        model = Line
        fields = '__all__'


class CartSerilaizer(serializers.ModelSerializer):
    lines = LineSerilaizer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ("lines", "id", "status", "owner_id")


class ProductCartSerializer(serializers.Serializer):

    product_id = serializers.CharField()
    cart_id = serializers.CharField()


class OrderSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
