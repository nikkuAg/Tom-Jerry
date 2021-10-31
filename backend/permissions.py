from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import *
from .encryption_util import *


class SentReceivePermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(obj)
        if decrypt(request.user.username) in [decrypt(obj.client.username), decrypt(obj.introducer.username)]:
            return True
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
