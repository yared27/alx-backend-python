from rest_framework import permissions

from messaging_app.chats.models import Conversation
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view,obj):
        return obj.user == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']:
            if isinstance(obj, Conversation):
                return request.user in obj.participants.all()
            
            if isinstance(obj, Message):
                return request.user in obj.conversation.participants.all()
        return False