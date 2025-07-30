from django.db import models
import uuid

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser

class UserRole(models.TextChoices):
    GUEST = 'guest', 'Guest'
    HOST = 'host', 'Host'
    ADMIN = 'admin', 'Admin'

class User(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=20, null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return f"{self.email} - {self.role}"
    
    #conversation model
class Conversation(models.Model):
        conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        participants = models.ManyToManyField(User, related_name='conversations')
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"Conversation {self.conversation_id} with {self.participants.count()} participants"
        
    
    # Message model
class Message(models.Model):
        message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
        sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
        message_body = models.TextField()
        sent_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"Message from {self.message_id} from {self.sender.email} in {self.conversation.conversation_id}"