from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_profile_creation_email(user_id, user_email):
    subject = "Profile Creation"
    message = f"Your profile with ID {user_id} has been created"
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
