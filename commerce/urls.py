from django.urls import path
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'commerce'

router = DefaultRouter()
router.register(r'^(?P<order_id>\d+)/order-items', OrderItemViewSet)
router.register(r'commerce/', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('showItemsCart/<int:cartId>/', get_cart_item_by_cart_id),
    path('store/', create_store),
    path('store/<int:userId>/', get_store),
    path('product/', product_list),
    path('product_list/', ProductListView.as_view()),
    path('product/find', search_product.as_view()),
    path('product/<int:pk>/', product_by_id),
    path('product/seller/<int:storeId>/', product_seller),
    path('cart/', cart_list),
    path('cart/<int:userId>/', cart_by_user_id),
    path('cartItem/', cart_item_list),
    path('cartItem/<int:cartId>', cartItem_by_cart_id),
    path('cartItem/id/<int:cartId>', cartItem_by_id),
    path('cartItemDetectSameItem/<int:cartId>/<int:productId>/', cartItem_detect_same_product),
    # path('productImg/', product_list),
    path('productImg/<int:productId>/', productImg_product_id),
    path('productImg/id/<int:id>/', productImg_by_id),
    path('productImg/find/<str:category>/', product_by_category),
    path('uploadFile/', upload_file.as_view()),
    path('deleteFile/<str:filename>', delete_file),
    path('filter/price/<int:minprice>/<int:maxprice>/', filter_range_price),
    path('filter/price/min/<int:minprice>/', filter_min_price),
    path('filter/price/max/<int:maxprice>/', filter_max_price),
    path('filter/rating/<int:rating>/', filter_rating),
    path('filter/condition/<str:condition>/', filter_condition),
    path('filter/price_and_rating/<int:minprice>/<int:maxprice>/<int:ratings>/', filter_price_and_rating),
    path('filter/price_and_condition/<int:minprice>/<int:maxprice>/<str:condition>/', filter_price_and_condition),
    path('filter/rating_and_condition/<int:rating>/<str:condition>/', filter_rating_and_condition),
    path('filter/<int:minprice>/<int:maxprice>/<int:rating>/<str:condition>/', filter_all),
]