from rest_framework import serializers

from market_backend.apps.accounts.models import SubCategory, Category, Product, User
from market_backend.apps.customer.models import Cart, Order, OrderedProducts
from market_backend.v0.accounts.serializers import GetFileSerializer, UserSerializer


class DeliveryBoyDetailsSerializer(serializers.ModelSerializer):
    profile_picture = GetFileSerializer(required=False)
    aadhaar_document = GetFileSerializer(required=False)
    license_document = GetFileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'username', 'email', 'address', 'profile_picture', 'aadhaar_document',
                  'license_document', 'is_available','pincode', )


class UpdateDeliveryBoyDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'address', 'pincode', 'profile_picture', 'aadhaar_document',
                  'license_document', 'is_available',)