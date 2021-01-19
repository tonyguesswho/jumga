from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid
from apps.product.models import Product
from apps.seller.models import Seller
# from decimal import Decimal as D


User = get_user_model()


class Cart(models.Model):
    """
    Cart object
    """
    # Baskets can be anonymously owned - hence this field is nullable.
    owner = models.ForeignKey(
        User,
        null=True,
        related_name='carts',
        on_delete=models.CASCADE,
        verbose_name=_("Owner"))

    OPEN, MERGED, SAVED, SUBMITTED = (
        "Open", "Merged", "Saved", "Submitted")
    STATUS_CHOICES = (
        (OPEN, _("Open - currently active")),
        (MERGED, _("Merged - superceded by another basket")),
        (SAVED, _("Saved - for items to be purchased later")),
        (SUBMITTED, _("Submitted - has been ordered at the checkout")),
    )
    status = models.CharField(
        _("Status"), max_length=128, default=OPEN, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_merged = models.DateTimeField(_("Date merged"), null=True, blank=True)
    date_submitted = models.DateTimeField(_("Date submitted"), null=True,
                                          blank=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lines = None

    def __str__(self):
        return _(
            "%(status)s cart (owner: %(owner)s, lines: %(num_lines)d)") \
            % {'status': self.status,
               'owner': self.owner,
               'num_lines': self.num_lines}

    def flush(self):
        """
            Remove all lines from cart.
        """
        self.lines.all().delete()

    def all_lines(self):
        """
        Return cart lines.

        """
        if self.id is None:
            return self.lines.none()
        if self._lines is None:
            self._lines = (
                self.lines
                .select_related('product')
                .order_by(self._meta.pk.name))
        return self._lines

    def add_product(self, product, price, quantity=1):
        line = self.lines.get_or_create(
            product=product, price=price)
        # line.quantity = max(0, line.quantity + quantity)
        # line.save()

        return line

    @property
    def num_lines(self):
        """Return number of lines"""
        return self.all_lines().count()

    @property
    def num_items(self):
        """Return number of items"""
        return sum(line.quantity for line in self.lines.all())


class Line(models.Model):
    """
    A line of a cart (product and a quantity)

    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name=_("Cart"))

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_lines',
        verbose_name=_("Product"))

    quantity = models.PositiveIntegerField(_('Quantity'), default=1)

    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='seller_lines', null=True)

    price_currency = models.CharField(
        _("Currency"), max_length=12, null=True)
    price = models.DecimalField(
        _('Price'), decimal_places=2, max_digits=12,
        null=True)

    created_at = models.DateTimeField(
        _("Date Created"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(
        _("Date Updated"), auto_now=True, db_index=True)


class Order(models.Model):
    """
    The main order model
    """

    # We track the site that each order is placed within
    seller = models.ForeignKey(
        Seller, verbose_name=_("Seller"),
        on_delete=models.CASCADE)

    cart = models.ForeignKey(
        Cart, verbose_name=_("Carts"), on_delete=models.CASCADE)

    user = models.ForeignKey(
        User, related_name='orders', null=True, blank=True,
        verbose_name=_("User"), on_delete=models.SET_NULL)

    address = models.CharField(max_length=100, blank=True)

    currency = models.CharField(
        _("Currency"), max_length=12, default="USD")
    total_price = models.DecimalField(
        _("Order total (inc. tax)"), decimal_places=2, max_digits=12)

    shipping_price = models.DecimalField(
        _("Shipping charge (inc. tax)"), decimal_places=2, max_digits=12,
        default=100)

    # Use this field to indicate that an order is on hold / awaiting payment
    status = models.CharField(_("Status"), max_length=100, blank=True)
    guest_email = models.EmailField(_("Guest email address"), blank=True)

    date_placed = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        app_label = 'order'
        ordering = ['-date_placed']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    @property
    def email(self):
        if not self.user:
            return self.guest_email
        return self.user.email
