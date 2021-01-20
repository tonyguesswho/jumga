from django.urls import path
from api.views.user import RegisterView, CustomAuthToken, Profileview
from api.views.seller import SellerView, SellerDetailView, \
    SellerPaymentView, PaymentConfirmView, StoreListView
from api.views.product import ProductView, ProductDetail
from api.views.payments import GetBanksView, AccountsView, AccountDetailView
from api.views.order import CartView, ProductCartView, OrderPaymentView, OrderConfirmView


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Jumga API",
        default_version='v1',
        description="Jumga",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

product_list = ProductView.as_view({
    'get': 'list',
    'post': 'create'
})
cart_list = CartView.as_view({
    'get': 'list',
    'post': 'create'
})


cart_detail = CartView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
product_detail = ProductView.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('me/', Profileview.as_view(), name='profile'),
    path('seller/', SellerView.as_view(), name='create_seller'),
    path('stores/', StoreListView.as_view(), name='list_stores'),
    path('seller/payment/', SellerPaymentView.as_view(), name='seller-payment'),
    path('order/payment/', OrderPaymentView.as_view(), name='order-payment'),
    path('seller/<slug:seller_id>/',
         SellerDetailView.as_view(), name='seller-detail'),
    path('account/<int:user_id>/',
         AccountDetailView.as_view(), name='account-detail'),
    path('seller/confirm-payment/<int:transaction_id>/<slug:trx_ref>/',
         PaymentConfirmView.as_view(),
         name='seller-confirm-payment'),
    path('order-payment/<int:transaction_id>/<slug:trx_ref>/',
         OrderConfirmView.as_view(),
         name='seller-confirm-payment'),
    path('getbanks/<str:country>/',
         GetBanksView.as_view(),
         name='banks'),
    path('account/',
         AccountsView.as_view(),
         name='add_account'),
    path('product', product_list),
    path('product/<int:pk>/', product_detail),
    path('cart/add/', ProductCartView.as_view(), name='add-product'),
    path('cart/', cart_list),
    path('cart/<int:pk>/', cart_detail),
    path('docs/', schema_view.with_ui('swagger',
                                      cache_timeout=0), name='schema-swagger-ui')
]
