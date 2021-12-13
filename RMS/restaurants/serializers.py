
from rest_framework import serializers
from . import models


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = ['title', 'address', 'town', 'post_code','country','longitude','latitude']



class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dish
        fields = ['name','price']