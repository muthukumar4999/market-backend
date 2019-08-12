from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from market_backend.apps.accounts.models import User, AuthUser, Category, SubCategory, \
    Media, Product  # , OrderCart, ConsumerProduct


class CreateFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('key', 'file_name', 'uploaded_at',)


class GetFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return settings.AWS_S3_BASE_LINK + obj.key

    class Meta:
        model = Media
        fields = ('id', 'file_name', 'url', 'key',)


class BasicUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'user_type', 'first_name', 'address')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if not user:
            msg = 'Unable to login with required credentials'
            raise ValidationError(msg)
        return user

    class Meta:
        model = User
        fields = ('username', 'password')


class UserSerializer(serializers.ModelSerializer):
    profile_picture = GetFileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile_picture')


class UserManagementSerializer(serializers.ModelSerializer):
    profile_picture = GetFileSerializer(required=False)
    aadhaar_document = GetFileSerializer(required=False)
    license_document = GetFileSerializer(required=False)

    class Meta:
        model = User
        fields = (
        'id', 'username', 'first_name', 'address', 'email', 'profile_picture', 'aadhaar_document', 'license_document')


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('token',)


class CategorySerializer(serializers.ModelSerializer):
    image = GetFileSerializer(required=False)

    class Meta:
        model = Category
        fields = ('id', 'name', 'image',)


class SubCategorySerializer(serializers.ModelSerializer):
    image = GetFileSerializer(required=False)

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category', 'image', 'unit', 'is_picture_available',
                  'is_type_available', 'is_color_available',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()
    wholesaler = serializers.SerializerMethodField()

    def get_wholesaler(self, obj):
        return {
            "id": obj.wholesaler.id,
            "name": obj.wholesaler.first_name,
            "address": obj.wholesaler.address
        }

    def get_category(self, obj):
        return {"id": obj.category.id,
                "name": obj.category.name}

    def get_sub_category(self, obj):
        return {"id": obj.sub_category.id,
                "name": obj.sub_category.name,
                "unit": obj.sub_category.unit}

    image = GetFileSerializer(required=False)

    class Meta:
        model = Product
        fields = ('__all__')


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')

# class AddWholesalerProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WholesalerProduct
#         fields = ('id', 'wholesaler', 'sub_category', 'product', 'price', 'quantity', 'is_out_of_stock',)
#
#
# class WholesalerProductSerializer(serializers.ModelSerializer):
#     wholesaler = UserSerializer()
#     sub_category = SubCategorySerializer()
#     product = ProductSerializer()
#     category = serializers.SerializerMethodField()
#
#     def get_category(self, obj):
#         return CategorySerializer(obj.sub_category.category).data
#
#     class Meta:
#         model = WholesalerProduct
#         fields = ('id', 'wholesaler', 'sub_category', 'product', 'price', 'quantity', 'is_out_of_stock', 'category')
#
#
# class ListWholesalerProductSerializer(serializers.ModelSerializer):
#     product_name = serializers.SerializerMethodField()
#     store_name = serializers.SerializerMethodField()
#     quantity = serializers.SerializerMethodField()
#     current_price = serializers.SerializerMethodField()
#     contact_number = serializers.SerializerMethodField()
#
#     def get_product_name(self, obj):
#         return obj.product.name
#
#     def get_store_name(self, obj):
#         return f'{obj.wholesaler.first_name} {obj.wholesaler.last_name}'
#
#     def get_quantity(self, obj):
#         return f'{obj.quantity} {obj.product.unit}'
#
#     def get_current_price(self, obj):
#         return '0'
#
#     def get_contact_number(self, obj):
#         return obj.wholesaler.username
#
#     class Meta:
#         model = WholesalerProduct
#         fields = ('id', 'store_name', 'product_name', 'price', 'quantity', 'current_price', 'contact_number')
#
#
# class AdminConsumerProductListSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()
#     category_name = serializers.SerializerMethodField()
#     sub_category_name = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()
#     original_price = serializers.SerializerMethodField()
#
#     def get_name(self,obj):
#         return obj.product.name
#
#     def get_category_name(self, obj):
#         return obj.product.sub_category.category.name
#
#     def get_sub_category_name(self, obj):
#         return obj.product.sub_category.name
#
#     def get_image(self, obj):
#         return GetFileSerializer(obj.product.image).data
#
#     def get_original_price(self, obj):
#         return obj.wholesaler_product.price
#
#
#     class Meta:
#         model = ConsumerProduct
#         fields = ('id', 'name', 'category_name', 'sub_category_name', 'image', 'customer_price','original_price')
#
#
# class OrderCartSerializer(serializers.ModelSerializer):
#     is_out_of_stock = serializers.SerializerMethodField()
#
#     def get_is_out_of_stock(self, obj):
#         return obj.consumer_product.wholesaler_product.is_out_of_stock
#
#     class Meta:
#         model = OrderCart
#         fields = ('id', 'consumer_product', 'quantity', 'updated_at', 'is_out_of_stock')
