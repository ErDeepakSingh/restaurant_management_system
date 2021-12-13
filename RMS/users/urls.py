from django.urls import path
from .views import CustomUserLogin,CustomUserSignup, \
    BlacklistTokenUpdateView,\
    SunAdminList,\
    SubAdminCreateAPIView,\
    UsersListAdminView


app_name = 'users'

urlpatterns = [
    path('', CustomUserLogin.as_view(), name="login"),
    path('sign_up/', CustomUserSignup.as_view(), name="sign_up"),
    path('sub_admin_list/', SunAdminList.as_view(), name="sub_admin_list"),
    path('users_list_admin_view/', UsersListAdminView.as_view(), name="users_list_admin_view"),
    path('create_sub_admin/', SubAdminCreateAPIView.as_view(), name="create_sub_admin"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]