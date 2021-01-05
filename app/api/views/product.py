
from rest_framework import viewsets, generics
from apps.product.models import Product
from api.serializers.product import ProductSerilaizer
from api.utils.permissions import IsSeller


class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerilaizer
    permission_classes = [IsSeller]

    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.filter(seller=user.seller)
        return queryset


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilaizer
