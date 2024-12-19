from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
