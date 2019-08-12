from django.db import models

# Create your models here.
from market_backend.apps.accounts.models import User, Product, Media


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=10)
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']


class Order(models.Model):
    CASH = 'CASH'
    UPI = 'UPI'
    CARD = 'CARD'
    OTHERS = 'OTHERS'
    PAYMENT_TYPE = ((CASH, CASH),
                    (UPI, UPI),
                    (CARD, CARD),
                    (OTHERS, OTHERS))
    PENDING = 'PENDING'
    PACKED = 'PACKED'
    PICKUPED = 'PICKUPED'
    DELIVERED = 'DELIVERED'

    ORDER_STATUS = ((PENDING, PENDING),
                    (PACKED, PACKED),
                    (PICKUPED, PICKUPED),
                    (DELIVERED, DELIVERED))

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_user')
    order_id = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_item = models.IntegerField()
    address = models.TextField()
    delivery_time = models.CharField(max_length=20)
    order_time = models.DateTimeField(auto_now_add=True)
    contact = models.CharField(max_length=10)
    contact_name = models.CharField(max_length=10, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)

    pickup_address = models.TextField(null=True, blank=True)

    order_status = models.CharField(max_length=30, choices=ORDER_STATUS, default=PENDING, null=True)

    is_delivered = models.BooleanField(default=False)
    delivered_time = models.DateTimeField(null=True, blank=True)
    delivery_boy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivery_user', null=True,
                                     blank=True)
    paid_by = models.CharField(max_length=30, choices=PAYMENT_TYPE, null=True, blank=True)
    upi_id = models.CharField(max_length=30, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id


class OrderedProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.CharField(max_length=10)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField(null=True)
    is_admin_buyed = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
