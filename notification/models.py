from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)      
    def __str__(self):
        return str({self.username})
    
 
    
    
class Notification(models.Model):
    recurring_choices = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    )
    notification_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField() 
    scheduled_datetime = models.DateTimeField()
    is_recurring = models.BooleanField(default=False)
    recurrence_interval = models.CharField(max_length=10, choices=recurring_choices, blank=True, null=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.content}"

