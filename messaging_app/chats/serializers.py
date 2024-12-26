from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerialzer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    password_hash = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=20)
    role = serializers.CharField(max_length=10)
    created_at = serializers.DateTimeField()   

    class Meta:
        model = User
        fileds = ['user_id','first_name','last_name','email','password_hash','phone_number','role','created_at']

        
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
