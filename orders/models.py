from django.db import models
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _


from accounts.models import CustomUser

from accounts.models import Address
from products.models import Products


# Create your models here.


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    order_date = models.DateTimeField(verbose_name=_("Order Date"), auto_now_add=True, editable=False)
    last_modify = models.DateTimeField(verbose_name=_("Last Modify"), auto_now=True, editable=False)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)



    @property
    def get_order_items(self):
        order_items = OrderDetail.objects.filter(order=self.id)
        return order_items

    @property
    def total_price(self):
        order_detail = self.get_order_items
        order_total_price = 0
        for item in order_detail:
            order_total_price += item.total_price
        return order_total_price

    def __str__(self):
        return f"Order{self.id}"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.PROTECT)
    product = models.ForeignKey(Products, verbose_name=_("Product Name"), on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, editable=False)

    class Meta:
        verbose_name_plural = "Order Details"

    @property
    def total_price(self):
        if self.price and self.quantity:
            return self.price * self.quantity
        else:
            return 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.price is None:
            self.price = self.product.price
            self.save()

    def __str__(self):
        return f"Order Details ID: {self.id}"


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True, blank=True)

    @classmethod
    def get_cart_item(cls, user):
        return cls.objects.filter(user=user)

