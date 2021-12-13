from django.urls import path
from .views import RestaurantListAPIView, \
    DishDetailCBV,\
    DishListAdminView,\
    RestaurantListAdminView,\
    RestaurantDistanceApiView


urlpatterns = [

    path('list/',RestaurantListAPIView.as_view(),name='Restaurant_list'),
    path('restaurant_list_admin_view/',RestaurantListAdminView.as_view(),name='restaurant_list_admin_view'),
    path('dish_list_admin_view/',DishListAdminView.as_view(),name='dish_list_admin_view'),
    path('dish_detail/',DishDetailCBV.as_view(),name='dish_detail'),
    path('restaurant_distance_api_view/', RestaurantDistanceApiView.as_view(), name="restaurant_distance_api_view"),

]