from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import PostModel
from django.conf import settings

@receiver(post_save, sender=PostModel)
def send_post_creation_notification(sender, instance, created, **kwargs):
    if created:
        # print("inside signal")
        print(instance.author.email)
        subject = 'New Post Created'
        message = f'A new post titled "{instance.title}" has been created.'
        from_email = settings.EMAIL_HOST_USER 
        # print(from_email)
        recipient_list = [instance.author.email]  
        # print(recipient_list)
        send_mail(subject, message, from_email, recipient_list)