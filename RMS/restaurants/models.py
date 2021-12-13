from django.db import models
from django.contrib.auth import get_user_model

class Restaurant(models.Model):
    title=models.CharField(verbose_name="Restaurant Name/Title",max_length=150,null=True,blank=True)
    address = models.CharField(verbose_name="Address",max_length=100, null=True, blank=True)
    town = models.CharField(verbose_name="Town/City",max_length=100, null=True, blank=True)
    post_code = models.CharField(verbose_name="Post Code",max_length=8, null=True, blank=True)
    country = models.CharField(verbose_name="Country",max_length=100, null=True, blank=True)
    longitude = models.CharField(verbose_name="Longitude",max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude",max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.title}'


class Dish(models.Model):
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    name=models.CharField(verbose_name="Dish Name",max_length=100, null=True, blank=True)
    price=models.CharField(verbose_name="Price",max_length=100, null=True, blank=True)
    created_by=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}->{self.restaurant}'