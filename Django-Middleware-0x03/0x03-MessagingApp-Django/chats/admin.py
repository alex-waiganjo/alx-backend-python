from django.contrib import admin
from .models import Message, Notification, User, Conversation


admin.site.register(Message)
admin.site.register(User)
admin.site.register(Conversation)



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "timestamp")
    ordering = ("-timestamp",)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "is_read", "timestamp")
    ordering = ("-timestamp",)