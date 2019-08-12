from rest_framework import serializers

from market_backend.apps.accounts.models import SubCategory, Category, Product, User
from market_backend.apps.customer.models import Cart, Order, OrderedProducts
from market_backend.v0.accounts.serializers import GetFileSerializer, UserSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    image = GetFileSerializer(required=False)

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'image')


class CustomerSubCategorySerializer(serializers.ModelSerializer):
    image = GetFileSerializer(required=False)

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'image', 'is_picture_available')


class CustomerCategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()
    image = GetFileSerializer(required=False)

    def get_sub_categories(self, obj):
        return CustomerSubCategorySerializer(SubCategory.objects.filter(category=obj.id), many=True).data

    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'sub_categories')


class CustomerCategoryDetailsSerializer(serializers.ModelSerializer):
    image = GetFileSerializer(required=False)

    class Meta:
        model = Category
        fields = ('id', 'name', 'image',)


class CustomerProductSerializer(serializers.ModelSerializer):
    category = CustomerCategorySerializer()
    sub_category = CustomerSubCategorySerializer()
    image = GetFileSerializer(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'sub_category', 'image', 'quantity', 'p_color', 'description', 'sbs_price',)


class CartSerializer(serializers.ModelSerializer):
    product = CustomerProductSerializer()
    image = GetFileSerializer(required=False)

    class Meta:
        model = Cart
        fields = ('__all__')


class OrderedProductsSerializer(serializers.ModelSerializer):
    product = CustomerProductSerializer(required=False)
    image = GetFileSerializer(required=False)

    class Meta:
        model = OrderedProducts
        fields = ('__all__')


class OrderSerializer(serializers.ModelSerializer):
    ordered_products = serializers.SerializerMethodField()
    customer = UserSerializer(required=False)
    delivery_boy = UserSerializer(required=False)

    def get_ordered_products(self, obj):
        queryset = OrderedProducts.objects.filter(order=obj)
        if queryset:
            return OrderedProductsSerializer(queryset, many=True).data
        return []

    class Meta:
        model = Order
        fields = ('__all__')


class CustomerDetailsSerializer(serializers.ModelSerializer):
    profile_picture = GetFileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'username', 'email', 'address', 'profile_picture', 'is_available', 'pincode','referral_code')


class UpdateCustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'address', 'pincode', 'profile_picture', 'aadhaar_document',
                  'license_document', 'is_available',)
