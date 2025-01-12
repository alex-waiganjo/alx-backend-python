import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.CharFilter(
        field_name='conversation__conversation_id')
    sender = django_filters.CharFilter(field_name='sender__user_id')
    sent_after = django_filters.DateTimeFilter(
        field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(
        field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'sent_after', 'sent_before']