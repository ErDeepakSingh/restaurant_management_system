
from rest_framework import viewsets,permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class AdminAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [JWTAuthentication]

    def has_permission(self, request, view):
        user = request.user
        if user:
            return user.is_superuser
        return False


class SubAAAdminAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [JWTAuthentication]

    def has_permission(self, request, view):
        user = request.user
        if user:
            print('user.is_staff',type(user.is_staff))
            print('user.is_staff',user.is_staff)
            print('user.is_superuser',type(user.is_superuser))
            print('user.is_superuser',user.is_superuser)
            if user.is_staff==True and user.is_superuser==False:
                return user.is_staff
        return False

class SubAdminAuthenticationPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        print("user",user)
        if request.method in permissions.SAFE_METHODS:
            return True
        if user.is_superuser:
            False
        return user.is_staff and obj.created_by == user


