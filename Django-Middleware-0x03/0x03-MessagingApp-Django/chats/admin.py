from django.contrib import admin
from .models import Message, User, Conversation


admin.site.register(Message)
admin.site.register(User)
admin.site.register(Conversation)
