from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Adding a full_name field for convenience
    full_name = serializers.SerializerMethodField()
    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender_name', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def validate(self, data):
        if not data.get('participants'):
            raise serializers.ValidationError("At least one participant is required for a conversation.")
        return data
