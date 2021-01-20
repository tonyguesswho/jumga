
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from apps.product.models import Product
from apps.seller.models import Seller
from api.serializers.product import ProductSerilaizer
from rest_framework.views import APIView
# from api.utils.permissions import IsSeller


# class ProductView(viewsets.ModelViewSet):
#     serializer_class = ProductSerilaizer
#     # permission_classes = [IsSeller]

#     def get_queryset(self):
#         # user = self.request.user
#         store = self.request.query_params.get('store', None)
#         print(store, "Store url")
#         seller = Seller.objects.get(url=store)
#         queryset = Product.objects.filter(seller=seller)
#         return queryset


class ProductView(APIView):
    """
    Get products
    """
    # serializer_class = ProductSerilaizer

    def get(self, request, *args, **kwargs):
        """
        """
        try:
            store = request.query_params.get('store')
            seller = Seller.objects.get(url=store)
            products = Product.objects.filter(seller=seller)
            return Response(ProductSerilaizer(products, many=True).data, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilaizer
