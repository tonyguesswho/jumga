from django.db import models
from django.contrib.auth import get_user_model
import uuid
from apps.seller.models import Seller


User = get_user_model()


class Product(models.Model):
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE)

    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=50, decimal_places=2)

    title = models.CharField(max_length=255)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
