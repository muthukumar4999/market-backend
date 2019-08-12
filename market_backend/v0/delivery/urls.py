from django.urls import path

from market_backend.v0.delivery import views

urlpatterns = [
    path('update_document/', views.UpdateDocumentProof.as_view(), name='update-document-proof'),
    path('user_details', views.DeliveryBoyDetails.as_view(), name='delivery-boy-details'),
    path('myorders', views.DeliveryOrderList.as_view(), name='delivery-boy-order'),
    path('myorders/<int:order_id>', views.DeliveryOrderByID.as_view(), name='delivery-boy-order-by-id'),
]
