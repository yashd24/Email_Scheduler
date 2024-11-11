#send mail function
from django.core.mail import send_mail

sender_email = 'yash.test.noreply@gmail.com'
password = 'Skull1324'

try:
    send_mail(
        'Email Notification',
        'notification.content',  # Ensure you're passing the actual content here, not a string 'notification.content'
        sender_email,
        ['yashd2024@gmail.com'],  # Pass recipient email as a list or tuple
        auth_user=sender_email,
        auth_password=password,
        fail_silently=False,
    )
    print("Email sent successfully")
except Exception as e:
    print("An error occurred while sending email:", str(e))