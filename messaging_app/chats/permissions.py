from rest_framework import permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view,obj):
        return obj.user == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):

        conversation = getattr(obj, 'conversation', obj)

        return request.user in conversation.participants.all() if conversation else False
