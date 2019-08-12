from django.contrib import admin

# Register your models here.
from market_backend.apps.customer.models import Cart, Order, OrderedProducts


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('customer', 'product', 'quantity')


class OrderedProductsAdminInline(admin.TabularInline):
    model = OrderedProducts
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('order_id','customer')
    readonly_fields = ('created_at', 'updated_at')
    inlines = (OrderedProductsAdminInline,)


admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
