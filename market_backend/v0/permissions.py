from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from rest_framework import status, permissions
from rest_framework.exceptions import APIException

from market_backend.apps.accounts.models import User, AuthUser
from market_backend.validator.errorcodemapping import ErrorMessage
from market_backend.validator.errormapping import ErrorCode


class UnauthorizedAccess(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"message": ErrorMessage.UNAUTHORIZED_ACCESS, "status": "failed",
                      "code": ErrorCode.UNAUTHORIZED_ACCESS}


class IsAllowedUser(permissions.IsAuthenticated):
    def __init__(self, *user_list):
        self.user_list = user_list

    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.user_type not in self.user_list:
            raise UnauthorizedAccess
        return True


class CustomAuthentication(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if username and password:
                user = User._default_manager.get_by_natural_key(username)
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
                else:
                    return None
            else:
                authorization = request.META['HTTP_AUTHORIZATION']
                if not authorization:
                    return None
                else:
                    token = authorization.split(' ')[1]
                    try:
                        return (AuthUser.objects.get(token=token, is_expired=False).user, None)
                    except AuthUser.DoesNotExist:
                        return None
        except Exception:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
