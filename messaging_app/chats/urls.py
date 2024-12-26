from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversation', ConversationViewSet, basename='conversation')
router.register(r'message', MessageViewSet, basename='message')


urlpatterns = [
    path('', include(router.urls)),
]