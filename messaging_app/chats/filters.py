import django_filters
from .models import Message
from django.contrib.auth.models import User

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    start_time = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    
    class Meta:
        model = Message
        fields = ['sender', 'start_time', 'end_time']