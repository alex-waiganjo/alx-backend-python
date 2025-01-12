from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message,Notification
@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    Signal to create a notification for the receiver when a new message is sent.
    """
    if created:  
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f"You have a new message from {instance.sender.username}."
        )
