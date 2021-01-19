from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid


class Rider(models.Model):
    email = models.EmailField(max_length=255, unique=True)

    name = models.CharField(max_length=255)

    country = models.CharField(max_length=255)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    subaccount_id = models.CharField(_('account_id'), max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
