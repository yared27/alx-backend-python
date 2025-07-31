from django.urls import include, path
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename ='conversation')
# Nested route for messages under conversations

conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
]
