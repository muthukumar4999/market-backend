from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _

from .models import User, AuthUser, Category, SubCategory, Media, Product  # , ConsumerProduct, OrderCart


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': (
             'first_name', 'last_name', 'email', 'user_type', 'address', 'referral_code', 'referred_by')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'address',
                'user_type',

            )}
         ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['username', 'type', 'is_active']
    list_filter = []

    def type(self, obj):
        if obj.user_type == User.ADMIN:
            return 'Admin'
        elif obj.user_type == User.CUSTOMER:
            return 'Customer'
        elif obj.user_type == User.DELIVERY_MAN:
            return 'Delivery man'
        elif obj.user_type == User.WHOLESALER:
            return 'Whole saler'
        else:
            return 'User'


class AuthUserAdmin(admin.ModelAdmin):
    model = AuthUser
    list_display = ['user', 'token', 'is_expired']


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name', ]


class SubCategoryAdmin(admin.ModelAdmin):
    model = SubCategory
    list_display = ['name', 'category']


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name', 'sub_category', 'wholesaler', 'is_out_of_stock']


class MediaAdmin(admin.ModelAdmin):
    model = Media
    list_display = ['key', 'file_name', 'uploaded_at']


#
# class ConsumerProductAdmin(admin.ModelAdmin):
#     model = ConsumerProduct
#     list_display = ['product', 'wholesaler_product', 'customer_price', 'is_drafted', 'is_published',]
#
# class OrderCartAdmin(admin.ModelAdmin):
#     model = OrderCart
#     list_display = ['consumer', 'consumer_product', 'quantity']

admin.site.register(User, CustomUserAdmin)
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Media, MediaAdmin)
# admin.site.register(ConsumerProduct, ConsumerProductAdmin)
# admin.site.register(OrderCart, OrderCartAdmin)
admin.site.site_url = 'http://market-backend.herokuapp.com/api/v0/docs/'
