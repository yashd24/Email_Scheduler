# Generated by Django 5.0.3 on 2024-03-17 15:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_alter_customuser_email_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='id',
        ),
        migrations.AddField(
            model_name='notification',
            name='notifcation_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
