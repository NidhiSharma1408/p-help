from rest_framework import permissions
from userauth.models import UserProfile

class IsSender(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.profile == obj.sender
    def has_permission(self,request,view):
        return request.user.is_authenticated

class IsReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.profile == obj.receiver
    def has_permission(self,request,view):
        return request.user.is_authenticated
