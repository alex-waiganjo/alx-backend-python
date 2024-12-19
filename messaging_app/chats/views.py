from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Conversation, Message
from .serializers import UserSerialzer, ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ViewSet):
    # List Conversations
    def list(self, request):
        get_conversations = Conversation.objects.all()
        serializer_class = ConversationSerializer
        serializer = serializer_class(instance=get_conversations, many=True)
        return Response(data=serializer.data)

    # Create Conversation(s)
    def create(self, request):
        serializer_class = ConversationSerializer
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ViewSet):
    # List Messages
    def list(self, request):
        get_messages = Message.objects.all()
        serializer_class = MessageSerializer
        serializer = serializer_class(instance=get_messages, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # Create Messages
    def create(self, request):
        serializer_class = MessageSerializer
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
