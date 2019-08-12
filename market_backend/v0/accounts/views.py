import datetime
import os
from functools import partial
import hashlib

import requests
from boto3 import Session
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.timezone import utc
from rest_framework import views, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from market_backend.apps.accounts.models import User, AuthUser, Category, SubCategory, \
    Media, Product  # , OrderCart, ConsumerProduct
from market_backend.apps.customer.models import Order, OrderedProducts
from market_backend.v0.accounts import serializers
from market_backend.v0.accounts.utils import AccountsUtils, FileUploadUtils
from market_backend.v0.constants import EmailConstant
from market_backend.v0.customer.serializers import OrderSerializer
from market_backend.v0.utils import Utils


class LoginView(views.APIView):
    """
       Login View allows the user to login into the application
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        To verify the authorized user and login them to the application
        :param request:
        :return:
        """
        validate_user = serializers.LoginSerializer(data=request.data)
        if validate_user.is_valid():
            user = validate_user.validated_data
            # old_tokens = AuthUser.objects.filter(user=user, is_expired=True)
            # if old_tokens:
            #     old_tokens.delete()
            #
            # AuthUser.objects.filter(user=user).update(is_expired=True)
            new_session = AuthUser(user=user)
            new_session.token = Utils.generate_token()
            new_session.save()
            serializer = serializers.AuthUserSerializer(new_session)
            return Utils.dispatch_success(request, serializer.data)
        else:
            return Utils.dispatch_failure(request, "UNAUTHORIZED_ACCESS", validate_user.errors)


class AddUser(views.APIView):
    """
    Add User Serializer
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        request_data = 
        {
        "username" : 9876543210,
        "user_type": "WHOLSESALER", # or 'CUSTOMER'
        "name": "STORE_NAME",
        "password": "Test@123",
        "address":"Address"
        }
        """
        try:
            data = request.data
            try:
                User.objects.get(username=data["username"])
            except User.DoesNotExist:
                user = User(username=data["username"],
                            user_type=data["user_type"],
                            first_name=data["name"],
                            address=data.get("address", ''))
                user.save()
                if data.get('email'):
                    user.email = data['email']
                user.set_password(data['password'])
                if user.user_type == User.CUSTOMER:
                    if data.get('referral_code'):
                        referred_user = User.objects.filter(referral_code=data['referral_code'])
                        if referred_user:
                            user.referred_by = referred_user
                    user.referral_code = f"{user.first_name[:4].upper()}" \
                        f"{(int(hashlib.sha256(user.username.encode('utf-8')).hexdigest(), 16) % 10 ** 6)}"
                user.save()
                return Utils.dispatch_success(request, ['SUCCESS'])
            else:
                return Utils.dispatch_failure(request, 'VALIDATION_ERROR')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class CategoryList(views.APIView):
    """
    Category List
    """

    def get(self, request, *args, **kwargs):
        """
        Return the list of categories
        :param request:
        :return:
        """
        try:
            is_all_category = request.GET.get('all', None)
            is_sub_category = request.GET.get('sub_category', None)
            if is_all_category:
                category_list = Category.objects.all()
            else:
                user = request.user
                user_type = user.user_type
                if user_type == User.WHOLESALER:
                    products = Product.objects.filter(wholesaler=user)
                    category_list = [product.sub_category.category for product in
                                     products]
                    category_list = set(category_list)
                else:
                    category_list = Category.objects.all()
            serializer = serializers.CategorySerializer(category_list, many=True, context={"user": request.user,
                                                                                           'is_sub_category': is_sub_category})
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})

    # def post(self, request, *args, **kwargs):
    #     """
    #     Create a new category
    #     :param request:
    #     :return:
    #     """
    #     try:
    #         serializer = serializers.CategorySerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #         else:
    #             return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
    #         return Utils.dispatch_success(request, serializer.data)
    #     except Exception as e:
    #         print(e)
    #         return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


# class CategoryDetails(views.APIView):
#     """
#     Category Details
#     """
#
#     def get(self, request, category_id, *args, **kwargs):
#         """
#         Get the particular category details
#         :param request:
#         :param category_id: int
#         :return:
#         """
#         try:
#             category = Category.objects.get(id=category_id)
#             serializer = serializers.CategorySerializer(category)
#             return Utils.dispatch_success(request, serializer.data)
#         except Category.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def put(self, request, category_id):
#         """
#         Update a particular Category
#         :param request:
#         :param category_id: category id
#         :return:
#         """
#         try:
#             category = Category.objects.get(id=category_id)
#             serializer = serializers.CategorySerializer(category, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
#             return Utils.dispatch_success(request, serializer.data)
#         except Category.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class SubCategoryList(views.APIView):
    """
    Sub Category List
    """

    def get(self, request, category_id):
        """
        Return the list of sub categories
        :param request:
        :param category_id:
        :return:
        """
        try:
            is_all_sub_category = request.GET.get('all', None)
            if is_all_sub_category:
                sub_category_list = SubCategory.objects.filter(category=category_id)
            else:
                user = request.user
                user_type = user.user_type
                if user_type == User.WHOLESALER:
                    products = Product.objects.filter(wholesaler=user, sub_category__category=category_id)
                    sub_category_list = [product.sub_category for product in
                                         products]
                    sub_category_list = set(sub_category_list)
                else:
                    sub_category_list = SubCategory.objects.filter(category=category_id)
            serializer = serializers.SubCategorySerializer(sub_category_list, many=True, context={"user": request.user})
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})

    # def post(self, request, category_id):
    #     """
    #     Create a new sub category
    #     :param request:
    #     :param category_id:
    #     :return:
    #     """
    #     try:
    #         data = request.data
    #         if SubCategory.objects.filter(category=category_id, name__iexact=data['name']):
    #             return Utils.dispatch_failure(request, "ITEM_ALREADY_EXISTS")
    #         data['category'] = category_id
    #         serializer = serializers.SubCategorySerializer(data=data)
    #         if serializer.is_valid():
    #             serializer.save()
    #         else:
    #             return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
    #         return Utils.dispatch_success(request, serializer.data)
    #     except Exception as e:
    #         print(e)
    #         return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


# class SubCategoryDetails(views.APIView):
#     """
#     Sub Category Details
#     """
#
#     def get(self, request, category_id, sub_category_id):
#         """
#         Get the particular sub category details
#         :param request:
#         :param category_id: int
#         :param sub_category_id: int
#         :return:
#         """
#         try:
#             sub_category = SubCategory.objects.get(id=sub_category_id)
#             serializer = serializers.SubCategorySerializer(sub_category)
#             return Utils.dispatch_success(request, serializer.data)
#         except SubCategory.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def put(self, request, category_id, sub_category_id):
#         """
#         Update a particular Sub Category
#         :param request:
#         :param category_id: category id
#         :param sub_category_id: sub_category id
#         :return:
#         """
#         try:
#             sub_category = SubCategory.objects.get(id=sub_category_id)
#             serializer = serializers.SubCategorySerializer(sub_category, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
#             return Utils.dispatch_success(request, serializer.data)
#         except SubCategory.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class ProductList(views.APIView):
    """
    Product List
    """

    def get(self, request, sub_category_id):
        """
        returns the list of products
        :param request:
        :param sub_category_id: sub_category_id
        :note:
        for recently added use -  recent=true query param
        pagination added use - page_number = 1
        Page size is customizable - page_size = 10
        :return:
        """
        try:
            if request.user.user_type == User.WHOLESALER:
                queryset = Product.objects.filter(sub_category=sub_category_id, wholesaler=request.user)
            else:
                if request.GET.get('recent', None):
                    queryset = Product.objects.filter(is_edited=True, is_drafted=False).order_by('-updated_at')
                else:
                    queryset = Product.objects.filter(sub_category=sub_category_id)
            page_size = request.GET.get('page_size', None)
            if page_size:
                page_size = int(page_size)
            else:
                page_size = 10

            page_number = request.GET.get('page_number', None)
            if page_number:
                page_number = int(page_number)
            else:
                page_number = 1

            if queryset:
                paginator = Paginator(queryset, per_page=page_size)

                queryset = paginator.page(page_number)

                serializer = serializers.ProductSerializer(queryset, many=True)
            response_data = {
                "data": serializer.data if queryset else [],
                "current_page": page_number,
                "page_size": page_size,
                "total_pages": paginator.num_pages if queryset else 1
            }
            return Utils.dispatch_success(request, response_data)

        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})

    def post(self, request, sub_category_id):
        """
        creates a new product
        :param request:
        :param sub_category_id: sub_category_id
        :request_data
        {
            "name": "Product_name",
            "category": 10,
            "sub_category": 10,
            "image": 10,
            "price":100.50,
            "quantity":10,
            "p_type": "16 GB, 32 GB, 64 GB",
            "p_color": "Green, Blue, Yellow",
            "description": "It is a secret description"
        }
        :return:
        """
        try:
            data = request.data
            data['wholesaler'] = request.user.id
            serializer = serializers.AddProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class ProductDetails(views.APIView):
    """
    Product Details
    """

    def get(self, request, product_id):
        """
        Returns a particular product based on sub_category id
        :param request:
        :param product_id: product_id
        :return:
        """
        try:
            product = Product.objects.get(id=product_id)
            serializer = serializers.ProductSerializer(product)
            return Utils.dispatch_success(request, serializer.data)
        except Product.DoesNotExist:
            return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})

    def put(self, request, product_id=None):
        """
        Updates a particular product
        :param request:
        :param product_id: product_id
        For save option used
        {
        "is_drafted":True, # if save
        }
        For publish used
        {
        "is_published":True, # if save and publish
        }
        for price
        {
        "sbs_price" : 11100
        }


        -----------------

        for publish all

        param = publish_all = true
        data = {
                "product_list":[10,11,12,13,14,15]
               }
        :return:
        """
        try:
            if not product_id and request.GET.get('publish_all'):
                for p_id in request.data['product_list']:
                    product = Product.objects.get(id=p_id)
                    product.is_drafted = False
                    product.is_edited = False
                    product.is_published = True
                    product.save()
                return Utils.dispatch_success(request, 'SUCCESS')
            else:
                data = request.data
                product = Product.objects.get(id=product_id)
                if data.get('is_published'):
                    data['is_drafted'] = False
                    data['is_edited'] = False
                if data.get('price'):
                    if request.user.user_type == User.WHOLESALER and product.price != data['price']:
                        data['is_edited'] = True
                        data['is_drafted'] = False
                        data['is_published'] = False

                serializer = serializers.AddProductSerializer(product, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
                    return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
                return Utils.dispatch_success(request, serializer.data)
        except Product.DoesNotExist:
            return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


# class WholesalerProductList(generics.ListCreateAPIView):
#     """
#     Wholesaler Product List
#     """
#     serializer_class = serializers.AddWholesalerProductSerializer
#
#     def get(self, request, *args, **kwargs):
#         """
#         returns the list of products
#         :param request:
#         :return:
#         """
#         try:
#             sub_category = request.GET.get('sub_category', None)
#             if request.user.user_type == User.WHOLESALER:
#                 if sub_category:
#                     queryset = WholesalerProduct.objects.filter(wholesaler=request.user, sub_category=sub_category)
#                 else:
#                     queryset = WholesalerProduct.objects.filter(wholesaler=request.user)
#             else:
#                 if sub_category:
#                     queryset = WholesalerProduct.objects.filter(sub_category=sub_category)
#                 else:
#                     queryset = WholesalerProduct.objects.all()
#
#             page_size = request.GET.get('page_size', None)
#             if page_size:
#                 page_size = int(page_size)
#             else:
#                 page_size = 10
#
#             page_number = request.GET.get('page_number', None)
#             if page_number:
#                 page_number = int(page_number)
#             else:
#                 page_number = 1
#
#             paginator = Paginator(queryset, per_page=page_size)
#
#             queryset = paginator.page(page_number)
#             serializer = serializers.WholesalerProductSerializer(queryset, many=True)
#             response_data = {
#                 "data": serializer.data,
#                 "current_page": page_number,
#                 "page_size": page_size,
#                 "total_pages": paginator.num_pages
#             }
#             return Utils.dispatch_success(request, response_data)
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def post(self, request, *args, **kwargs):
#         """
#         creates a new wholesaler product
#         :param request:
#         :return:
#         """
#         try:
#
#             data = request.data
#             if WholesalerProduct.objects.filter(wholesaler=request.user, product=data['product']):
#                 return Utils.dispatch_failure(request, "ITEM_ALREADY_EXISTS")
#             data['wholesaler'] = request.user.id
#             serializer = serializers.AddWholesalerProductSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
#             return Utils.dispatch_success(request, serializer.data)
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#
# class WholesalerProductDetails(views.APIView):
#     """
#     Wholesaler Product Details
#     """
#
#     def get(self, request, wholesaler_product_id):
#         """
#         Returns a particular wholesaler product based on sub_category id
#         :param request:
#         :param wholesaler_product_id: wholesaler_product_id
#         :return:
#         """
#         try:
#             wholesaler_product = WholesalerProduct.objects.get(id=wholesaler_product_id)
#             serializer = serializers.WholesalerProductSerializer(wholesaler_product)
#             return Utils.dispatch_success(request, serializer.data)
#         except WholesalerProduct.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def put(self, request, wholesaler_product_id):
#         """
#         Updates a particular Wholesaler product
#         :param request:
#         :param wholesaler_product_id: wholesaler_product_id
#         :return:
#         """
#         try:
#             wholesaler_product = WholesalerProduct.objects.get(id=wholesaler_product_id)
#             serializer = serializers.WholesalerProductSerializer(wholesaler_product, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
#             return Utils.dispatch_success(request, serializer.data)
#         except WholesalerProduct.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def delete(self, request, wholesaler_product_id):
#         """
#         Delete the request wholesaler product
#         :param request:
#         :param wholesaler_product_id:
#         :return:
#         """
#         try:
#             wholesaler_product = WholesalerProduct.objects.get(id=wholesaler_product_id)
#             wholesaler_product.delete()
#             return Utils.dispatch_success(request, 'SUCCESS')
#         except WholesalerProduct.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#

# class RecentlyAddedWholeSaleProduct(views.APIView):
#     """
#     Recently added Wholesaler Products
#     """
#
#     def get(self, request):
#         """
#           Returns the List of Recently added Wholesaler Products
#          :param request:
#          :return:
#          """
#         try:
#             wholesaler_products = WholesalerProduct.objects.filter(is_out_of_stock=False).order_by('updated_at')
#             page_size = request.GET.get('page_size', None)
#             if page_size:
#                 page_size = int(page_size)
#             else:
#                 page_size = 10
#
#             page_number = request.GET.get('page_number', None)
#             if page_number:
#                 page_number = int(page_number)
#             else:
#                 page_number = 1
#
#             paginator = Paginator(wholesaler_products, per_page=page_size)
#
#             queryset = paginator.page(page_number)
#             serializer = serializers.ListWholesalerProductSerializer(queryset, many=True)
#             response_data = {
#                 "data": serializer.data,
#                 "current_page": page_number,
#                 "page_size": page_size,
#                 "total_pages": paginator.num_pages
#             }
#             return Utils.dispatch_success(request, response_data)
#
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#
# class ForgotPasswordView(views.APIView):
#     """
#     Forgot Password Request Handler
#     """
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         """
#         To create a forgot password request and make a entry in the table
#         :param request:
#         :return:
#         """
#         try:
#             username = request.data.get("username", None)
#
#             # Check if username parameter is on request
#             if not username:
#                 return Utils.dispatch_failure(request, 'DATA_NOT_FOUND')
#
#             # Check if username is valid
#             if not Utils.validate_email_address(username):
#                 return Utils.dispatch_failure(request, 'VALIDATION_ERROR')
#
#             # Check if username is registered
#             user = User.objects.filter(username=username,organization__is_active=True)
#             if not user:
#                 return Utils.dispatch_failure(request, 'EMAIL_NOT_FOUND')
#             if user.count() > 1:
#                 return Utils.dispatch_failure(request, 'MULTIPLE_EMAIL_FOUND')
#
#             # Generate unique token
#             token = Utils.generate_unique_token()
#             user = user.first()
#
#             # Save forgot password details in table
#             forgot_password = ForgotPasswordRequest(user=user, token=token,
#                                                     expires_at=datetime.datetime.utcnow().replace(
#                                                         tzinfo=utc) + datetime.timedelta(minutes=30),
#                                                     )
#             forgot_password.save()
#
#             subject = EmailConstant.FORGOT_PASSWORD_SUBJECT
#             body = EmailConstant.FORGOT_PASSWORD_BODY.format(link=settings.FORGOT_PASSWORD_URL + token + '/')
#             Utils.send_mail([username, ], subject=subject, body="", html_message=Utils.build_email_body(user, body))
#
#         except Exception:
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR')
#
#         return Utils.dispatch_success(request, 'EMAIL_SEND')
#
#
# class ChangePasswordView(views.APIView):
#     """
#     Change password based on the Forgot Password Request
#     """
#     permission_classes = (AllowAny,)
#
#     def get(self, request, token):
#         """
#         To Verify the Forgot Password request Token is expired or not
#         :param request:
#         :param token:
#         :return:
#         """
#         try:
#             forgot_password_request = ForgotPasswordRequest.objects.get(token=token)
#             expiry_time = forgot_password_request.expires_at
#             current_time = datetime.datetime.utcnow().replace(tzinfo=utc)
#             if expiry_time >= current_time and not forgot_password_request.is_expired:
#                 return Utils.dispatch_success(request, 'TOKEN_VALID')
#             else:
#                 return Utils.dispatch_failure(request, 'TOKEN_EXPIRED')
#         except ForgotPasswordRequest.DoesNotExist:
#             return Utils.dispatch_failure(request, 'TOKEN_EXPIRED')
#
#     def post(self, request, token=None):
#         """
#         Updates User password
#         :param request:
#         :param token:
#         :return:
#         """
#         try:
#             if token:
#                 forgot_password_request = ForgotPasswordRequest.objects.get(token=token)
#                 if forgot_password_request.is_expired:
#                     return Utils.dispatch_failure(request, 'TOKEN_EXPIRED')
#                 user = forgot_password_request.user
#                 forgot_password_request.is_expired = True
#                 forgot_password_request.save()
#             else:
#                 user = request.user
#                 data = {
#                     "username": user.username,
#                     "password": request.data.get('old_password')
#                 }
#                 validate_user = serializers.LoginSerializer(data=data)
#                 if not validate_user.is_valid():
#                     return Utils.dispatch_failure(request, 'INVALID_OLD_PASSWORD')
#
#             password = request.data.get('password')
#             user.set_password(password)
#             user.save()
#         except ForgotPasswordRequest.DoesNotExist:
#             return Utils.dispatch_failure(request, 'TOKEN_EXPIRED')
#         return Utils.dispatch_success(request, 'PASSWORD_RESET_SUCCESSFUL')
#
#
# class CreatePasswordView(views.APIView):
#     """
#     To verify the User Creation Token and Update the User Password
#     """
#     permission_classes = (AllowAny,)
#
#     def get(self, request, token):
#         """
#         To Verify the User creation Token is expired or not
#         :param request:
#         :param token:
#         :return:
#         """
#         try:
#             user_creation_request = UserCreationRequest.objects.get(token=token)
#             if not user_creation_request.is_expired:
#                 response = {
#                     'username': user_creation_request.user.username
#                 }
#                 return Utils.dispatch_success(request, response)
#             else:
#                 return Utils.dispatch_failure(request, 'TOKEN_EXPIRED')
#         except UserCreationRequest.DoesNotExist:
#             return Utils.dispatch_failure(request, 'TOKEN_EXPIRED')
#
#     def post(self, request, token):
#         """
#         Creates password for the user for First time.
#         :param request:
#         :param token:
#         :return:
#         """
#         try:
#             user_creation_request = UserCreationRequest.objects.get(token=token)
#             if user_creation_request.is_expired:
#                 return Utils.dispatch_failure(request, 'TOKEN_EXPIRED')
#             password = request.data.get('password')
#             u = User.objects.get(id=user_creation_request.user.id)
#             u.set_password(password)
#             u.save()
#             user_creation_request.is_expired = True
#             user_creation_request.save()
#             return Utils.dispatch_success(request, 'PASSWORD_CREATED_SUCCESSFUL')
#         except Exception:
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR')


class UserList(views.APIView):
    """
    User list view
    """

    def get(self, request):
        """
        Returns the list of users
        :param request:
        :return:
        """
        try:
            user_type_list = request.GET.getlist('user_type', [])
            queryset = User.objects.filter(is_active=True)

            if user_type_list:
                queryset = queryset.filter(user_type__in=user_type_list).order_by('id')

            if queryset:
                serializer = serializers.BasicUserInfoSerializer(queryset, many=True)
                return Utils.dispatch_success(request, serializer.data)
            return Utils.dispatch_success(request, 'DATA_NOT_FOUND')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class Me(views.APIView):
    """
    Returns Current user details
    """

    def get(self, request):
        """
        Returns the list of users
        :param request:
        :return:
        """
        try:
            serializer = serializers.BasicUserInfoSerializer(request.user)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class UserExists(views.APIView):
    """
    User Exists check API
    """

    def post(self, request):
        """
        Post the User email to verify the user exists or not
        :param request:
        :return:
        """
        return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND') if User.objects.filter(
            username=request.data['username']) else Utils.dispatch_success(request, ["SUCCESS"])


class FileUpload(generics.CreateAPIView):
    """
    helper api to upload the files
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.CreateFileUploadSerializer

    def post(self, request, *args, **kwargs):
        """
        Uploads the file and return the uploaded file details
        :param request:
        :return:
        """
        try:
            print(f'request data - {request.data}')
            key = request.data.get('key', None)

            if key is not None:
                FileUploadUtils.deleteFile(key)

            print(f'request file - {request.FILES}')

            file = request.FILES['file']
            filename = file.name
            file_extension = filename.split('.')[1]

            extension = FileUploadUtils.getContentType(file_extension)

            session = Session(aws_access_key_id=settings.AWS_ACCESS_KEY,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                              region_name=settings.AWS_REGION_NAME)

            s3 = session.resource('s3')

            file_key = FileUploadUtils.getFileKey()

            res = s3.Bucket(settings.AWS_BUCKET_NAME).put_object(Key=file_key, Body=file, ContentType=extension,
                                                                 ACL='public-read')

            data = {'key': file_key, 'file_name': filename}
            serializer = serializers.CreateFileUploadSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

            media = Media.objects.get(key=file_key)
            media_serializer = serializers.GetFileSerializer(media)
            return Utils.dispatch_success(request, media_serializer.data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'FILE_UPLOAD_FAILED', {"error": str(e)})


# class ProductBasedWholersalerList(views.APIView):
#     """
#     Product Based Wholesaler List
#     """
#
#     def get(self, request, product_id):
#         """
#         Returns the List of Wholesaler unser the particular product exculeds out of stock list
#         :param request:
#         :param product_id:
#         :return:
#         """
#         try:
#             wholesaler_product = WholesalerProduct.objects.filter(product=product_id, is_out_of_stock=False)
#             serializer = serializers.ListWholesalerProductSerializer(wholesaler_product, many=True)
#             return Utils.dispatch_success(request, serializer.data)
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#
# class OrderCartView(generics.ListCreateAPIView):
#     # need to move to consumer
#     """
#     For User Cart Functionality
#     """
#     serializer_class = serializers.OrderCartSerializer
#
#     def get(self, request, *args, **kwargs):
#         """
#         Returns the cart List order cart of request user
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         try:
#             cart_items = OrderCart.objects.filter(consumer=request.user)
#             is_count = request.GET.get('count', None)
#             if is_count:
#                 return Utils.dispatch_success(request, {"count": cart_items.count()})
#
#             serializer = serializers.OrderCartSerializer(cart_items, many=True)
#             return Utils.dispatch_success(request, serializer.data)
#
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#
# class AdminConsumerProductList(views.APIView):
#     """
#     For Consumer Product Functionality
#     """
#
#     def get(self, request, product_id, *args, **kwargs):
#         """
#         Returns the List of consumer products of the request user
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         try:
#             return Utils.dispatch_success(request, '#Todo')
#
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def put(self, request, product_id):
#         """
#         Update or Create the Consumer Product
#         :param request:
#         :param product_id:
#         :return:
#         """
#         try:
#             data = request.data
#             wholesaler_product = WholesalerProduct.objects.get(id=data['wholesaler_product_id'])
#             product = Product.objects.get(id=product_id)
#             try:
#                 consumer_product = ConsumerProduct.objects.get(product=product_id)
#             except ConsumerProduct.DoesNotExist:
#                 consumer_product = ConsumerProduct(product=product,
#                                                    wholesaler_product=wholesaler_product,
#                                                    customer_price=data['customer_price'],
#                                                    is_drafted=data['is_drafted'],
#                                                    is_published=data['is_published'])
#             else:
#                 consumer_product.wholesaler_product =wholesaler_product
#                 consumer_product.customer_price = data['customer_price']
#                 consumer_product.is_drafted = data['is_drafted']
#                 consumer_product.is_published = data['is_published']
#             consumer_product.save()
#             return Utils.dispatch_success(request, 'SUCCESS')
#
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class StoreList(views.APIView):
    """
    :note:

    pagination added use - page_number = 1
    Page size is customizable - page_size = 10
    """

    def get(self, request):
        try:
            queryset = User.objects.filter(is_active=True, user_type=User.WHOLESALER).order_by('first_name')
            page_number = request.GET.get('page_number', 1)
            page_size = request.GET.get('page_size', 10)

            if queryset:
                paginator = Paginator(queryset, per_page=page_size)

                queryset = paginator.page(page_number)

                serializer = serializers.UserManagementSerializer(queryset, many=True)
            response_data = {
                "data": serializer.data if queryset else [],
                "current_page": page_number,
                "page_size": page_size,
                "total_pages": paginator.num_pages if queryset else 1
            }
            return Utils.dispatch_success(request, response_data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class StoreDetail(views.APIView):
    """Store object CRUD view"""

    def get(self, request, id):
        """
        Get particular store
        :param request:
        :param id:
        :return:
        """
        try:
            user = User.objects.get(id=id)
            return Utils.dispatch_success(request, serializers.BasicUserInfoSerializer(user).data)
        except User.DoesNotExist:
            return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})

    def put(self, request, id):
        """
        Update particular store
        :param request:
        :param id:
        :return:
        """
        try:
            user = User.objects.get(id=id)
            data = request.data
            serializer = serializers.BasicUserInfoSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Utils.dispatch_success(request, serializer.data)
            return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
        except User.DoesNotExist:
            return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})

    def delete(self, request, id):
        """
        Delete particular store
        :param request:
        :param id:
        :return:
        """
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Utils.dispatch_success(request, "SUCCESS")
        except User.DoesNotExist:
            return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class AllProductList(views.APIView):
    """
    All Product List
    """

    def get(self, request):
        """
        returns the list all the  productsbased on queryset
        :param request:
        :note:
        for not published -  not_published=true query param
        for published -  published=true query param
        pagination added use - page_number = 1
        Page size is customizable - page_size = 10
        :return:
        """
        try:
            if request.GET.get('not_published'):
                queryset = Product.objects.filter(is_drafted=True, is_published=False).order_by('-updated_at')
            elif request.GET.get('published'):
                queryset = Product.objects.filter(is_published=True).order_by('-updated_at')
            else:
                queryset = Product.objects.all().order_by('-updated_at')
            page_size = request.GET.get('page_size')
            if page_size:
                page_size = int(page_size)
            else:
                page_size = 10

            page_number = request.GET.get('page_number')
            if page_number:
                page_number = int(page_number)
            else:
                page_number = 1

            if queryset:
                paginator = Paginator(queryset, per_page=page_size)

                queryset = paginator.page(page_number)

                serializer = serializers.ProductSerializer(queryset, many=True)
            response_data = {
                "data": serializer.data if queryset else [],
                "current_page": page_number,
                "page_size": page_size,
                "total_pages": paginator.num_pages if queryset else 1
            }
            return Utils.dispatch_success(request, response_data)

        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class OrderList(views.APIView):
    def get(self, request):
        """
        for pending Orders
        param = order_status=pending

        for order history
        no param

        pagination added use - page_number = 1
        Page size is customizable - page_size = 10

        :param request:
        :return:
        """
        try:
            if request.GET.get('order_status') == 'pending':
                queryset = Order.objects.filter(order_status=Order.PENDING).order_by('order_time')
            else:
                queryset = Order.objects.all().exclude(order_status=Order.PENDING).order_by('-order_time')
            page_size = request.GET.get('page_size')
            if page_size:
                page_size = int(page_size)
            else:
                page_size = 10

            page_number = request.GET.get('page_number')
            if page_number:
                page_number = int(page_number)
            else:
                page_number = 1

            if queryset:
                paginator = Paginator(queryset, per_page=page_size)

                queryset = paginator.page(page_number)

                serializer = OrderSerializer(queryset, many=True)
            response_data = {
                "data": serializer.data if queryset else [],
                "current_page": page_number,
                "page_size": page_size,
                "total_pages": paginator.num_pages if queryset else 1
            }
            return Utils.dispatch_success(request, response_data)

        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class DeliveryBoyList(views.APIView):
    def get(self, request):
        """
        pagination added use - page_number = 1
        Page size is customizable - page_size = 10

        param = is_available = true

        :param request:
        :return:
        """
        try:
            if request.GET.get('is_available'):
                queryset = User.objects.filter(user_type=User.DELIVERY_MAN, is_available=True)
                return Utils.dispatch_success(request, serializers.BasicUserInfoSerializer(queryset, many=True).data)
            else:
                queryset = User.objects.filter(user_type=User.DELIVERY_MAN)
            page_size = request.GET.get('page_size')
            if page_size:
                page_size = int(page_size)
            else:
                page_size = 10

            page_number = request.GET.get('page_number')
            if page_number:
                page_number = int(page_number)
            else:
                page_number = 1

            if queryset:
                paginator = Paginator(queryset, per_page=page_size)

                queryset = paginator.page(page_number)

                serializer = serializers.UserManagementSerializer(queryset, many=True)
            response_data = {
                "data": serializer.data if queryset else [],
                "current_page": page_number,
                "page_size": page_size,
                "total_pages": paginator.num_pages if queryset else 1
            }
            return Utils.dispatch_success(request, response_data)

        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class OrderByID(views.APIView):
    def get(self, request, order_id):
        """
        Provide Order ID to get Details
        :param request:
        :param order_id:
        :return:
        """
        try:
            order_item = Order.objects.get(id=order_id)
            return Utils.dispatch_success(request, OrderSerializer(order_item).data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})

    def put(self, request, order_id):
        """
        {
        "order_status" : "PACKED"
        "delivery_boy" : 34
        "pickup_address" : "ANy Really Long ADdress"
        }
        :param request:
        :param order_id:
        :return:
        """
        try:
            order_item = Order.objects.get(id=order_id)
            data = request.data
            if data.get('order_status'):
                order_item.order_status = data['order_status']
            if data.get('delivery_boy'):
                order_item.delivery_boy = User.objects.get(id=data['delivery_boy'])
            if data.get('pickup_address'):
                order_item.pickup_address = data['pickup_address']
            order_item.save()

            return Utils.dispatch_success(request, OrderSerializer(order_item).data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class TodayRequirement(views.APIView):
    """
    Returns Today Requirement
    """

    def get(self, request):
        try:
            pending_orders = Order.objects.filter(order_status=Order.PENDING)
            data = {}
            for pending_order in pending_orders:
                for order_item in OrderedProducts.objects.filter(order=pending_order):
                    product = order_item.product
                    product_data = {'id': order_item.id,
                                    'name': product.name,
                                    'quantity': order_item.quantity,
                                    'per_item_price': order_item.price_per_item,
                                    'total_price': order_item.total_price,
                                    'is_admin_buyed': order_item.is_admin_buyed
                                    }
                    data.setdefault(order_item.product.wholesaler.first_name, []).append(product_data)
            return Utils.dispatch_success(request, data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})

    def put(self, request):
        """
        To Update Buyed need to send response
        {
        "order_products" : [1,2,3,4,5,6,7,8,9,10]
        }
        note: These id's are ordered_products
        :param request:
        :return:
        """
        try:
            data = request.data
            OrderedProducts.objects.filter(id__in=data['order_products']).update(is_admin_buyed=True)
            return Utils.dispatch_success(request, 'SUCCESS')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
