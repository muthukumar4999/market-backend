from django.urls import path

from market_backend.v0.customer import views

urlpatterns = [
    path('fav/', views.Favourites.as_view(), name='fav-sub-categories'),
    path('products/recent/', views.RecentProductList.as_view(), name='products-recent-items'),
    path('products/random/', views.RandomProductList.as_view(), name='products-random-items'),
    path('category/', views.CustomerCategoryList.as_view(), name='customer-categories'),
    path('search/', views.CustomerSearchList.as_view(), name='customer-search'),
    path('products/under/sub_category/<int:sub_category>/', views.CustomerProductListBasedOnSubCategory.as_view(),
         name='product-under-sub-category'),
    path('products/under/category/<int:category>/', views.CustomerProductListBasedOnCategory.as_view(),
         name='product-under-category'),

    path('cart/items/', views.CartList.as_view(), name='cart-items'),
    path('cart/<int:cart_id>/', views.RemoveCart.as_view(), name='remove-cart-item'),
    path('cart/add-to-cart/', views.AddToCart.as_view(), name='add-to-cart'),

    path('order/all/', views.OrderList.as_view(), name='order-list'),
    path('order/place-order/', views.PlaceOrder.as_view(), name='place-order'),
    path('order/<int:order_id>/', views.OrderByID.as_view(), name='order-by-id'),

    path('referral_check/<slug:referral_code>/', views.ReferralCheck.as_view(), name='referral-check'),

    path('user_details', views.CustomerDetails.as_view(), name='customer-details'),
]
