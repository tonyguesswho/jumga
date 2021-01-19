from django.db import models
from django.core.validators import validate_unicode_slug
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.delivery.models import Rider

import uuid

User = get_user_model()


class Seller(models.Model):
    user = models.OneToOneField(
        User, related_name='seller', on_delete=models.CASCADE)

    rider = models.OneToOneField(
        Rider, related_name='rider', on_delete=models.CASCADE, null=True)
    name = models.CharField(_('Store name'), max_length=255)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(
        _('Active'), default=False,
        help_text=_('Designates whether this seller should be treated as'
                    'active.'))
    url = models.CharField(_('Store url'), max_length=50, unique=True,
                           validators=[validate_unicode_slug])

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    country_code = models.CharField(_('alpha 2 country code'), max_length=3)

    currency = models.CharField(_('currency'), max_length=3, default='USD')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
