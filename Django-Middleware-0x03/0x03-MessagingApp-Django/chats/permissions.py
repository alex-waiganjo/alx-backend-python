from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsMessageSender(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user


class IsParticipantOfConversation(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        elif hasattr(obj, 'sender'):
            return request.user == obj.sender or request.user in obj.conversation.participants.all()
        return False
