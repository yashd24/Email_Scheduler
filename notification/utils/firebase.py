import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings


def send_push_notification(token, title, body):
    cred = credentials.Certificate(settings.FIREBASE_APP['credential_file'])
    firebase_admin.initialize_app(cred)

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    response = messaging.send(message)
    print('Successfully sent message:', response)
