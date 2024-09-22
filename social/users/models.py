from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, null=True)
    verification_sent = models.DateTimeField(null=True)
    date = models.DateField(auto_now_add=True)
    img = models.CharField(max_length=200)
    
    def add_notification(self, text, url):
        Notification(user=self, text=text, url=url).save()

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    url = models.CharField(max_length=100)
    is_watched = models.BooleanField(default=False)

