from django.urls import path

from market_backend.v0.accounts import views

urlpatterns = [

    path('login/', views.LoginView.as_view(), name='login'),

    path('users/', views.UserList.as_view(), name='user-list'),
    
    path('add-user/', views.AddUser.as_view(), name='add-user'),
    
    path('me/', views.Me.as_view(), name='me'),

    # path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    #
    # path('create-password/<slug:token>/', views.CreatePasswordView.as_view(), name='create-password'),
    #
    # path('change-password/<slug:token>/', views.ChangePasswordView.as_view(), name='change-password'),
    #
    # path('reset-password/', views.ChangePasswordView.as_view(), name='reset-password'),

    path('user-check/', views.UserExists.as_view(), name='user-check'),

    path('file-upload/', views.FileUpload.as_view(), name='file-upload'),


    path('stores/', views.StoreList.as_view(), name='store-list'),
    path('stores/<int:id>/', views.StoreDetail.as_view(), name='store-details'),

    path('category/', views.CategoryList.as_view(), name='category-list'),

    # path('category/<int:category_id>/', views.CategoryDetails.as_view(), name='category-details'),

    path('category/<int:category_id>/sub_category/', views.SubCategoryList.as_view(), name='sub-category-list'),
    # path('category/<int:category_id>/sub_category/<int:sub_category_id>/', views.SubCategoryDetails.as_view(),
    #      name='sub-category-details'),

    path('addproducts/<int:sub_category_id>/products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:product_id>/', views.ProductDetails.as_view(),
         name='product-details'),
    path('products/publish-all/', views.ProductDetails.as_view(),
         name='product-publish-all'),

    path('products/all/', views.AllProductList.as_view(), name='product-all-list'),

    path('orders/', views.OrderList.as_view(), name='admin-order-list'),
    path('order/<int:order_id>/', views.OrderByID.as_view(), name='admin-order-by-id'),

    #
    # path('wholesaler_product/recent/', views.RecentlyAddedWholeSaleProduct.as_view(),
    #          name='Recently-added-wholesaler-product-details'),

    path('delivery_boy/', views.DeliveryBoyList.as_view(), name='admin-delivery-list'),

    path('today_requirement/', views.TodayRequirement.as_view(), name='admin-today-requirement'),
]
