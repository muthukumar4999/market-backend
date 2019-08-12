import datetime

from django.core.paginator import Paginator
from rest_framework import views

from market_backend.apps.customer.models import Order
from market_backend.v0.customer.serializers import OrderSerializer
from market_backend.v0.delivery import serializers
from market_backend.apps.accounts.models import User, Media
from market_backend.v0.utils import Utils


class UpdateDocumentProof(views.APIView):
    """
    Update Proof Document
    """

    def put(self, request):
        """
        request_data:{
        "aadhaar_document":2,
        "license_document":3,
        }
        :param request:
        :return:
        """
        try:
            user = request.user
            data = request.data
            if user.user_type == User.DELIVERY_MAN:
                if data.get('aadhaar_document'):
                    user.aadhaar_document = Media.objects.get(id=data['aadhaar_document'])
                if data.get('license_document'):
                    user.license_document = Media.objects.get(id=data['license_document'])
                user.save()
            return Utils.dispatch_success(request, 'SUCCESS')
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class DeliveryBoyDetails(views.APIView):
    """
    Get Delivery Boy detail
    """

    def get(self, request):
        """
        :param request:
        :return:
        """
        try:
            user = request.user
            return Utils.dispatch_success(request, serializers.DeliveryBoyDetailsSerializer(user).data)
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
            serializer = serializers.UpdateDeliveryBoyDetailsSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Utils.dispatch_success(request, serializers.DeliveryBoyDetailsSerializer(user).data)
            return Utils.dispatch_failure(request, serializer.errors)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class DeliveryOrderList(views.APIView):
    def get(self, request):
        """
        pagination added use - page_number = 1
        Page size is customizable - page_size = 10
        -----------------------------------------------
        for Completed orders give param status=completed
        :param request:
        :return:
        """
        try:
            if request.GET.get('status') == 'completed':
                queryset = Order.objects.filter(delivery_boy=request.user, order_status=Order.DELIVERED)
            else:
                queryset = Order.objects.filter(delivery_boy=request.user,
                                                order_status__in=[Order.PACKED, Order.PICKUPED])

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

                serializer = OrderSerializer(queryset, many=True)
            response_data = {
                "data": serializer.data if queryset else [],
                "current_page": page_number,
                "page_size": page_size,
                "total_pages": paginator.num_pages if queryset else 1,
                "total" : len(queryset)
            }
            return Utils.dispatch_success(request, response_data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})


class DeliveryOrderByID(views.APIView):
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
        "order_status" : DELIVERED / PICKUPED
        "paid_by" : CASH / UPI
        "upi_id" : 14621849198541265621
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
                if data['order_status'] == Order.DELIVERED:
                    order_item.is_delivered = True
                    order_item.delivered_time = datetime.datetime.now()
            if data.get('paid_by'):
                order_item.paid_by = data['paid_by']
            if data.get('upi_id'):
                order_item.upi_id = data['upi_id']
            order_item.save()

            return Utils.dispatch_success(request, OrderSerializer(order_item).data)
        except Exception as e:
            print(e)
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
