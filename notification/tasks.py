from celery import shared_task
from django.core.mail import send_mail
from .models import Notification
from dotenv import load_dotenv
import os
import logging

load_dotenv()
sender_email = os.getenv('EMAIL')
logger = logging.getLogger(__name__)


@shared_task(name='send_notification')
def send_notification(notification_id):
    logger.info(
        f"Starting send_notification task for notification_id: {notification_id}")

    print("sendingggggggg")
    try:
        notification_data = Notification.objects.get(
            notification_id=notification_id)
        print(f'sending from{sender_email} to {notification_data.user.email}')

        if not notification_data.is_sent:
            send_mail(
                'Email Notification',
                notification_data.content,
                sender_email,
                recipient_list=[notification_data.user.email],
                fail_silently=False,
            )
            print('sent.........')
            notification_data.is_sent = True  # Mark notification as sent
            notification_data.save()

    except Exception as e:
        print(e)


@shared_task
def test():

    print('Executed test task')
    return "Executed test task"
