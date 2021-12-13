from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from .mixins import SerializeMixin,HttpResponseMixin,is_json
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from django.utils.translation import ugettext as _
from .serializers import RestaurantSerializer, DishSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from users.response import Response as response
from users.custom_permissions import AdminAuthenticationPermission,SubAdminAuthenticationPermission
from . models import Restaurant,Dish
import json
from .distance import get_distance,isvalid_latlong

class RestaurantListAPIView(ListAPIView):
    '''
        Method: GET
        URL: http://127.0.0.1:8000/restaurant/list
        AUTHORIZATION BEARER TOKEN: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM4ODE1ODY1LCJpYXQiOjE2Mzg4MTIyNjUsImp0aSI6IjYzOGFiMDY5OWFmZjQ4NmE4NzFmNmExMzI1MTc4NzlhIiwidXNlcl9pZCI6OH0.4Wjw27PvyLBUoAp2fFbx66us94BcI177PAhWgHFxj_g
        Response:[
                    {
                        "title": "Mc Donalds",
                        "address": "HOUSE NO :-151 , GALI NUMBER 18",
                        "town": "NEW DELHI",
                        "post_code": "261303",
                        "country": "India",
                        "longitude": "16.925168",
                        "latitude": "52.406374"
                    },
                    {
                        "title": "Punjab Grills",
                        "address": "U-52/22",
                        "town": "Gurugram",
                        "post_code": "221008",
                        "country": "India",
                        "longitude": "16.9251681",
                        "latitude": "52.406374"
                    }
                ]
    '''
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_view_name(self):
        return super().get_queryset()


class RestaurantListAdminView(ListAPIView):
    '''
    Method: GET
    URL: http://127.0.0.1:8000/restaurant/restaurant_list_admin_view
    AUTHORIZATION BEARER TOKEN: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM4ODE1ODY1LCJpYXQiOjE2Mzg4MTIyNjUsImp0aSI6IjYzOGFiMDY5OWFmZjQ4NmE4NzFmNmExMzI1MTc4NzlhIiwidXNlcl9pZCI6OH0.4Wjw27PvyLBUoAp2fFbx66us94BcI177PAhWgHFxj_g
    Response :[
            {
                "title": "Mc Donalds",
                "address": "HOUSE NO :-151 , GALI NUMBER 18",
                "town": "NEW DELHI",
                "post_code": "261303",
                "country": "India",
                "longitude": "16.925168",
                "latitude": "52.406374"
            },
            {
                "title": "Punjab Grills",
                "address": "U-52/22",
                "town": "Gurugram",
                "post_code": "221008",
                "country": "India",
                "longitude": "16.9251681",
                "latitude": "52.406374"
            }
        ]
    '''
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,SubAdminAuthenticationPermission]

    def get_queryset(self):
        """
        This view should return a list of all the Restaurant
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_superuser and user.is_staff:
            return Restaurant.objects.all()
        if user.is_staff:
            return Restaurant.objects.filter(created_by=user)

    def get_view_name(self):
        return super().get_queryset()


class DishListAdminView(ListAPIView):
    '''
    Method: GET
    URL: http://127.0.0.1:8000/restaurant/dish_list_admin_view
    AUTHORIZATION BEARER TOKEN: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM4ODE1ODY1LCJpYXQiOjE2Mzg4MTIyNjUsImp0aSI6IjYzOGFiMDY5OWFmZjQ4NmE4NzFmNmExMzI1MTc4NzlhIiwidXNlcl9pZCI6OH0.4Wjw27PvyLBUoAp2fFbx66us94BcI177PAhWgHFxj_g
    Response :[
                    {
                        "name": "Kadhai Chicken",
                        "price": "251"
                    },
                    {
                        "name": "Paneer do Pyaza",
                        "price": "300"
                    },
                    {
                        "name": "Burger",
                        "price": "150"
                    }
                ]
    '''
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,SubAdminAuthenticationPermission]

    def get_queryset(self):
        """
        This view should return a list of all the Dish
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_superuser and user.is_staff:
            return Dish.objects.all()
        if user.is_staff:
            return Dish.objects.filter(created_by=user)

    def get_view_name(self):
        return super().get_queryset()

class RestaurantDistanceApiView(APIView):
    '''
    Method: POST
    URL:http://127.0.0.1:8000/restaurant/restaurant_distance_api_view/
    REQUEST PARAMETER:{
                        "lattitude":52.2296756,
                        "longitude":21.0122287
                    }
    Expected Response :{
                        "Restaurant1": {
                            "title": "Mc Donalds",
                            "address": "HOUSE NO :-151 , GALI NUMBER 18",
                            "town": "NEW DELHI",
                            "post_code": "261303",
                            "country": "India",
                            "longitude": "16.925168",
                            "latitude": "52.406374",
                            "distance_from_user_in_km": "278.5455961306376"
                        },
                        "Restaurant2": {
                            "title": "Punjab Grills",
                            "address": "U-52/22",
                            "town": "Gurugram",
                            "post_code": "221008",
                            "country": "India",
                            "longitude": "16.9251681",
                            "latitude": "52.406374",
                            "distance_from_user_in_km": "278.54558935106695"
                        }
                    }
    '''

    serializer_class = RestaurantSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if "lattitude" in request.data and "longitude" in request.data and request.data['lattitude'] != "" and request.data['longitude'] != "":
            lattitude = request.data.get('lattitude')
            longitude = request.data.get('longitude')
            if isvalid_latlong(lattitude,longitude):
                try:
                    print("lattitude",lattitude)
                    print("longitude",longitude)
                    __resultdict={}
                    context={}
                    count=1
                    for restaurant in Restaurant.objects.all():
                        rest_key="Restaurant"+str(count)
                        rest_lattitude=float(restaurant.latitude)
                        rest_longitude=float(restaurant.longitude)
                        print(rest_lattitude,rest_longitude)
                        rest_distance=get_distance(lattitude,longitude,rest_lattitude,rest_longitude)
                        serialized_rest = RestaurantSerializer(restaurant).data
                        serialized_rest.update({'distance_from_user_in_km':str(rest_distance)})
                        context.update({rest_key:serialized_rest})
                        # print('serialized_rest',serialized_rest)
                        print('serialized_rest',type(serialized_rest))
                        count+=1
                    # print('context',context)
                    __resultdict=json.dumps(context)
                    # print("__resultdict",__resultdict)
                    # return Response(response.parsejson(_("Distance of Restaurants for given user is fetched successfully"), __resultdict, status=200))
                    return  HttpResponse(__resultdict,content_type='application/json',status=200)
                except Exception as e:
                    print(e)
                    return Response(response.parsejson(_("something went wrong please try again!"), "", status=404))
            else:
                return Response(response.parsejson(_("please provide valid lattitude/longitude value !"), "", status=404))
        else:
            return Response(response.parsejson(_("lattitude and longitude is required"), {}, status=404))




@method_decorator(csrf_exempt,name='dispatch')
class DishDetailCBV(HttpResponseMixin,SerializeMixin,View):
    '''
    Method: POST
    URL:
    REQUEST PARAMETER:{
                            "restaurant_id":1
                        }
    Expected Response :[
                        {
                            "restaurant": 1,
                            "name": "Burger",
                            "price": "150",
                            "created_by": 1,
                            "updated": "2021-12-13T03:58:36.566Z"
                        }
                    ]
    '''
    def get_object_by_id(self,restaurant_id):
        try:
            dish=Dish.objects.get(restaurant_id=restaurant_id)
        except Dish.DoesNotExist:
            dish=None
        return dish
    def post(self,request,*args,**kwargs):
        data=request.body
        valid_json=is_json(data)
        if not valid_json:
            self.render_to_http_response(json.dumps({'mesage':'Please provide json data only'}),status=400)
        pdata=json.loads(data)
        restaurant_id=pdata.get('restaurant_id',None)
        print('restaurant_id',restaurant_id)
        if restaurant_id is not None:
            restaurant=self.get_object_by_id(restaurant_id)
            if restaurant is None:
                json_data=json.dumps({'message':'The requested resource is not available Please provide correct ID'})
                return self.render_to_http_response(json_data,status=400)
            json_data=self.serialize([restaurant,])
            return self.render_to_http_response(json_data)
        querry_set=Dish.objects.all()
        json_data=self.serialize(querry_set)
        return self.render_to_http_response(json_data)






