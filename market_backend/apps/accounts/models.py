from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Media(models.Model):
    key = models.CharField(max_length=300)
    file_name = models.CharField(max_length=150)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return settings.AWS_S3_BASE_LINK + self.key + ' -------  ' + self.file_name


class User(AbstractUser):
    ADMIN = 'ADMIN'
    WHOLESALER = 'WHOLESALER'
    CUSTOMER = 'CUSTOMER'
    DELIVERY_MAN = 'DELIVERY_MAN'

    USER_TYPE = ((ADMIN, ADMIN),
                 (WHOLESALER, WHOLESALER),
                 (CUSTOMER, CUSTOMER),
                 (DELIVERY_MAN, DELIVERY_MAN),)

    user_type = models.CharField(choices=USER_TYPE, max_length=50)
    address = models.TextField(null=True, blank=True)
    pincode = models.CharField(null=True, max_length=6)
    referral_code = models.CharField(null=True, max_length=10)
    referred_by = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    aadhaar_document = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, related_name = 'aadhaar_document')
    license_document = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, related_name = 'license_document')
    is_available = models.BooleanField(default=True)
    profile_picture = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, related_name = 'profile_picture')

    def __str__(self):
        return self.username


class AuthUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=500)
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"


class SubCategory(models.Model):
    KG = "Kg"
    G = "g"
    M = "m"
    NO = "No(s)"
    L = "l"

    UNIT = ((KG, KG),
            (G, G),
            (NO, NO),
            (M, M),
            (L, L))
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.CharField(max_length=20, choices=UNIT, default=NO)
    is_picture_available = models.BooleanField(default=False)
    is_type_available = models.BooleanField(default=False)
    is_color_available = models.BooleanField(default=False)
    is_fav = models.BooleanField(default=False)
    fav_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Sub Categories"


class Product(models.Model):
    name = models.CharField(max_length=500,default="")
    wholesaler = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    p_type = models.CharField(max_length=200, null=True, blank=True)
    p_color = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_out_of_stock = models.BooleanField(default=False)

    sbs_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_drafted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name




