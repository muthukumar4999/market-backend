import datetime
from random import shuffle

from django.core.paginator import Paginator
from rest_framework import views
from rest_framework.permissions import AllowAny

from market_backend.apps.customer.models import Cart, Order, OrderedProducts
from market_backend.v0.customer import serializers
from market_backend.apps.accounts.models import User, SubCategory, Category, Product, Media
from market_backend.v0.utils import Utils


class Favourites(views.APIView):
    """Returns the Favourite sub category"""

    def get(self, request):
        """

        :param request:
        :return:
        """
        try:
            queryset = SubCategory.objects.filter(is_fav=True).order_by('fav_order')
            return Utils.dispatch_success(request, serializers.FavoriteSerializer(queryset, many=True).data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class RecentProductList(views.APIView):
    """
    All Product List
    """

    def get(self, request):
        """
        returns the list all the  productsbased on queryset
        :param request:
        :note:

        pagination added use - page_number = 1
        Page size is customizable - page_size = 10
        :return:
        """
        try:
            queryset = Product.objects.filter(is_published=True).order_by('-updated_at')
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

                serializer = serializers.CustomerProductSerializer(queryset, many=True)
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


class RandomProductList(views.APIView):
    """
    All Product List
    """

    def get(self, request):
        """
        returns the list all the  products based on queryset
        :param request:
        :note:

        pagination added use - page_number = 1
        Page size is customizable - page_size = 10
        :return:
        """
        try:
            queryset = Product.objects.filter(is_published=True)
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

                serializer = serializers.CustomerProductSerializer(queryset, many=True)
                data = serializer.data
                shuffle(data)
            else:
                data = []

            response_data = {
                "data": data,
                "current_page": page_number,
                "page_size": page_size,
                "total_pages": paginator.num_pages if queryset else 1
            }
            return Utils.dispatch_success(request, response_data)

        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class CustomerCategoryList(views.APIView):
    """
    Customer Category List
    """

    def get(self, request, *args, **kwargs):
        """
        Return the list of categories
        :param request:
        :return:
        """
        try:
            category_list = Category.objects.all()
            serializer = serializers.CustomerCategorySerializer(category_list, many=True)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class CustomerSearchList(views.APIView):
    """
    Customer Search Now works only on includes
    """

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        send ?text="searchtext" as param
        pagination added use - page_number = 1
        Page size is customizable - page_size = 10
        :return:
        """
        try:
            search = request.GET.get('text', '')
            queryset = Product.objects.filter(is_published=True, name__icontains=search)
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

                serializer = serializers.CustomerProductSerializer(queryset, many=True)
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


class CustomerProductListBasedOnSubCategory(views.APIView):
    """
    Customer Search Now works only on includes
    """

    def get(self, request, sub_category, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        pagination added use - page_number = 1
        Page size is customizable - page_size = 10
        :return:
        """
        try:
            # search = request.GET.get('text', '')
            queryset = Product.objects.filter(is_published=True, sub_category=sub_category)
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

                serializer = serializers.CustomerProductSerializer(queryset, many=True)
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


class CustomerProductListBasedOnCategory(views.APIView):
    """
    Customer Search Now works only on includes
    """

    def get(self, request, category_id, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        pagination added use - page_number = 1
        Page size is customizable - page_size = 10
        :return:
        """
        try:
            # search = request.GET.get('text', '')
            queryset = Product.objects.filter(is_published=True, category=category_id)
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

                serializer = serializers.CustomerProductSerializer(queryset, many=True)
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


class AddToCart(views.APIView):
    """
    Add / Update the Cart
    """

    def post(self, request):
        """
        post_data = { product_id : 1,
        "quantity": 10,
        "comments": "Isdgfsdgdgsdgdsgds",
        "image":3
        },
        send quantity = 0 to remove item from cart
        :param request:
        :return:
        """
        try:
            cart = Cart.objects.filter(customer=request.user, product=request.data['product_id']).first()
            if cart:
                if request.data['quantity']:
                    cart.quantity = request.data['quantity']
                    cart.save()
                else:
                    cart.delete()
            else:
                cart = Cart(customer=request.user,
                            product=Product.objects.get(id=request.data['product_id']),
                            quantity=request.data['quantity'],
                            image=Media.objects.get(id=request.data['image']) if request.data.get('image') else None,
                            comments=request.data.get('comments', ''),
                            )
                cart.save()

            return Utils.dispatch_success(request, 'SUCCESS')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class RemoveCart(views.APIView):
    """
    delete a Cart item
    """

    def delete(self, request, cart_id):
        """
        :param request:
        :return:
        """
        try:
            cart = Cart.objects.filter(id=cart_id).first()
            if cart:
                cart.delete()
            return Utils.dispatch_success(request, 'SUCCESS')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class CartList(views.APIView):
    def get(self, request):
        try:
            cart_items = Cart.objects.filter(customer=request.user)
            total = 0.0
            for cart_item in cart_items:
                total += float(cart_item.product.sbs_price) * float(cart_item.quantity)
            delivery_charge = 50
            response_data = {
                "data": serializers.CartSerializer(cart_items, many=True).data,
                "delivery_charge": delivery_charge,
                "total": total,
                "total_with_delivery_charge": total + delivery_charge
            }
            return Utils.dispatch_success(request, response_data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class OrderList(views.APIView):
    def get(self, request):
        try:
            order_items = Order.objects.filter(customer=request.user).order_by('-order_time')
            return Utils.dispatch_success(request, serializers.OrderSerializer(order_items, many=True).data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class OrderByID(views.APIView):
    def get(self, request, order_id):
        try:
            order_items = Order.objects.get(id=order_id)
            return Utils.dispatch_success(request, serializers.OrderSerializer(order_items).data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class PlaceOrder(views.APIView):
    def post(self, request):
        """
        {
        "address" : "ADDRESS",
        "delivery_time" : "4PM - 5PM",
        "pincode" : "PINCODE",
        "contact" : "98932782398",
        "contact_name" : "HJBGFHJSBJA",
        "delivery_charge": 50
        }
        :param request:
        :return:
        """
        try:
            cart_items = Cart.objects.filter(customer=request.user)
            today = datetime.date.today()
            order = Order(
                customer=request.user,
                order_id=f'ORDER{today.year}{int(today.month):02}{int(today.day):02}{Order.objects.all().count():07}',
                total_price=sum(
                    [float(cart_item.product.sbs_price) * float(cart_item.quantity) for cart_item in cart_items]),
                total_item=len(cart_items),
                address=request.data['address'],
                delivery_time=request.data['delivery_time'],
                contact=request.data['contact'],
                contact_name=request.data['contact_name'],
                pincode=request.data['pincode'],
                delivery_charge=request.data['delivery_charge']
            )
            order.save()
            request.user.address = request.data['address']
            request.user.pincode = request.data['pincode']
            request.user.save()
            for cart_item in cart_items:
                ordered_product = OrderedProducts(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_per_item=cart_item.product.sbs_price,
                    image=cart_item.image,
                    total_price=float(cart_item.product.sbs_price) * float(cart_item.quantity),
                    comments=cart_item.comments
                )
                ordered_product.save()
                cart_item.delete()
            return Utils.dispatch_success(request, 'SUCCESS')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class ReferralCheck(views.APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, referral_code):
        try:
            User.objects.get(referral_code=referral_code)
            return Utils.dispatch_success(request, 'SUCCESS')
        except User.DoesNotExist:
            return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class CustomerDetails(views.APIView):
    """
    Get Customer detail
    """

    def get(self, request):
        """
        :param request:
        :return:
        """
        try:
            user = request.user
            return Utils.dispatch_success(request, serializers.CustomerDetailsSerializer(user).data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})

    def put(self, request):
        """
        :param request:
        :return:
        """
        try:
            user = request.user
            data = request.data
            serializer = serializers.UpdateCustomerDetailsSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Utils.dispatch_success(request, serializers.CustomerDetailsSerializer(user).data)
            return Utils.dispatch_failure(request, serializer.errors)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
