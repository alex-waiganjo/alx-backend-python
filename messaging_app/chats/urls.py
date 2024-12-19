from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router =DefaultRouter()
router = DefaultRouter()
router.register(r'conversation', ConversationViewSet, basename='conversation')
router.register(r'message', MessageViewSet, basename='message')


urlpatterns = [
    path('', include(router.urls)),
]