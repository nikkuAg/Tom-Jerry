from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import *
from .encryption_util import *


class SentReceivePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # print("inside has permission", request.method)
            return request.user.is_staff
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        users = User.objects.all()
        print(users)
        print(obj)
        for user in users:
            if decrypt(user.username) in [decrypt(obj.client), decrypt(obj.introducer)]:
                print("came inside !!")
                return request.method == 'DELETE' and obj.client == request.user or request.user == obj.introducer
        return request.user.is_staff


class AuditPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class ClientSentPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
