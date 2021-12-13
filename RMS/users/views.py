from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.db.models import Q
from rest_framework import permissions
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from .response import Response as response
from . models import User,UserDetail
from .serializers import CustomUserSerializer,UserDetailSerializer
from .custom_permissions import AdminAuthenticationPermission,SubAdminAuthenticationPermission



class CustomUserSignup(APIView):
    '''
    Method: POST
    URL:   http://127.0.0.1:8000/user/sign_up/
    REQUEST PARAMETER:  {
                        "email":"spk@gmail.com",
                        "password": "pass@123"
                        }
    Response :{
                "error": 0,
                "code": 1,
                "data": {
                    "email": "spk@gmail.com",
                    "is_staff": false,
                    "is_superuser": false
                },
                "msg": "Your account has been created successfully"
            }
    '''
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(response.parsejson(_("Your account has been created successfully"), json,  status=status.HTTP_201_CREATED))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomUserLogin(APIView):
    '''
    Method: POST
    URL:http://127.0.0.1:8000/user/
    REQUEST PARAMETER:{
                        "email":"deepak@gmail.com",
                        "password": "pass@123"
                        }
    Expected Response :{
                        "error": 0,
                        "code": 1,
                        "data": {
                            "email": "deepak@gmail.com",
                            "is_staff": true,
                            "is_superuser": true,
                            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzOTk3MTE1MywiaWF0IjoxNjM5MzY2MzUzLCJqdGkiOiI5YmViNmRjMWM1MmU0OTU1YmEwNWYxYjk4MTI1NDdiNiIsInVzZXJfaWQiOjF9.Bn9pge8AZO4j4bsDHkCsdYD6GwU6A-dCWSK237eWW2Y",
                            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM5MzY5OTUzLCJpYXQiOjE2MzkzNjYzNTMsImp0aSI6IjYxZTRlYzQzOTAwMzQzYzI4YjJhMDRiN2M4OGY5YzYwIiwidXNlcl9pZCI6MX0.APs6m-e0Ysv7kNmkizxiQB_GtOFBnAxW2722VQLCY2g"
                        },
                        "msg": "Login successfully"
                    }
    '''

    def post(self, request):
        if "email" in request.data and request.data['email'] != "":
            email = request.data.get('email')
            print("email",email)
            try:
                print("email",email)
                userObj = User.objects.get(Q(email__iexact=email))
            except Exception:
                return Response(response.parsejson(_("Email/Username does not exist"), "", status=404))
        else:
            return Response(response.parsejson(_("Email/Username is required"), {}, status=404))

        if "password" in request.data and request.data['password'] != "":
            password = request.data.get('password')
        else:
            return Response(response.parsejson(_("password is required"), {}, status=404))

        if (not userObj.check_password(password)):
            return Response(response.parsejson(_("Email/Username or password do not match"), "",status=status.HTTP_404_NOT_FOUND))

        if userObj.is_active == False:
            return Response(response.parsejson(_("Your account is inactive state, Please contact to administrator"), {}, status=404))

        userObj.last_login = timezone.now()
        userObj.save(update_fields=['last_login'])

        serialized_user = CustomUserSerializer(userObj).data
        __resultlist = dict(CustomUserSerializer(userObj).data.items())

        refresh = RefreshToken.for_user(userObj)
        __resultlist['refresh'] = str(refresh)
        __resultlist['access'] = str(refresh.access_token)
        return Response(response.parsejson(_("Login successfully"),__resultlist, 201))


class BlacklistTokenUpdateView(APIView):
    '''
    Method: POST
    URL: http://127.0.0.1:8000/user/logout/blacklist/
    REQUEST PARAMETER: {
                        "refresh_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzOTQ1MDU2NywiaWF0IjoxNjM4ODQ1NzY3LCJqdGkiOiJmNjhlM2Y4NzgxMTc0YmZlODhmM2VhN2YzY2ExMDJjYSIsInVzZXJfaWQiOjEwfQ.DRWr_bZB68XJnHZ7jeIICiYh18IbOmwSuRaLy9TWMqs"
                        }
    Expected Response :{
                        "error": 0,
                        "code": 0,
                        "data": {},
                        "msg": "You have been logged out successfully"
                        }
    '''
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            print(request.data)
            refresh_token = request.data["refresh"]
            print('refresh_token',refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(response.parsejson(_("You have been logged out successfully"), {},status=status.HTTP_205_RESET_CONTENT))
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)



class SunAdminList(ListAPIView):
    '''
    Method: GET
    URL:http://127.0.0.1:8000/user/sub_admin_list/

    Expected Response :[
                        {
                            "email": "deepak@gmail.com",
                            "is_staff": true,
                            "is_superuser": true
                        },
                        {
                            "email": "deekshaparmar19@gmail.com",
                            "is_staff": true,
                            "is_superuser": false
                        },
                        {
                            "email": "pqr@gmail.com",
                            "is_staff": true,
                            "is_superuser": false
                        }
                    ]
    '''
    queryset = User.objects.filter(is_staff=True)
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,AdminAuthenticationPermission]

    def get_view_name(self):
        return super().get_queryset()


class SubAdminCreateAPIView(CreateAPIView):
    '''
    Method: GET
    URL:http://127.0.0.1:8000/user/create_sub_admin/
    REQUEST PARAMETER: {
                        "email":"gls@gmail.com",
                        "password": "pass@123",
                        "is_staff":"True"
                        }
    Expected Response :{
                            "email": "gls@gmail.com",
                            "is_staff": true,
                            "is_superuser": false
                        }
    '''

    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,AdminAuthenticationPermission]

    def perform_create(self, serializer):
        # print(serializer)
        return serializer.save()


class UsersListAdminView(ListAPIView):
    '''
    Method: GET
    URL:http://127.0.0.1:8000/user/create_sub_admin/

    Expected Response :[
                        {
                            "email": "deepak@gmail.com",
                            "is_staff": true,
                            "is_superuser": true
                        },
                        {
                            "email": "deekshaparmar19@gmail.com",
                            "is_staff": true,
                            "is_superuser": false
                        },
                        {
                            "email": "abc@gmail.com",
                            "is_staff": false,
                            "is_superuser": false
                        },
                        {
                            "email": "qwe@gmail.com",
                            "is_staff": false,
                            "is_superuser": false
                        },
                        {
                            "email": "pqr@gmail.com",
                            "is_staff": true,
                            "is_superuser": false
                        },
                        {
                            "email": "spk@gmail.com",
                            "is_staff": false,
                            "is_superuser": false
                        },
                        {
                            "email": "gls@gmail.com",
                            "is_staff": true,
                            "is_superuser": false
                        }
                    ]
    '''

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,AdminAuthenticationPermission]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_superuser and user.is_staff:
            return User.objects.all()
        if user.is_staff:
            return User.objects.filter(created_by=user)
    def get_view_name(self):
        return super().get_queryset()



