from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerialzer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fileds = ['user_id','first_name','last_name','email','password_hash','phone_number','role','created_at','full_name']

        def full_name(self,obj):
            return f'{obj.first_name} {obj.last_name}'
        
        def validation_email(self, value):
            if '@yahoo.com' in value:
                raise serializers.ValidationError("Domain is unacceptable")
            return value
        
        
       


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
