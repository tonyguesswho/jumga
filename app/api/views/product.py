
from rest_framework import viewsets, generics
from apps.product.models import Product
from apps.seller.models import Seller
from api.serializers.product import ProductSerilaizer
# from api.utils.permissions import IsSeller


class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerilaizer
    # permission_classes = [IsSeller]

    def get_queryset(self):
        # user = self.request.user
        store = self.request.GET.get("store", None)
        seller = Seller.objects.get(url=store)
        queryset = Product.objects.filter(seller=seller)
        return queryset


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilaizer
