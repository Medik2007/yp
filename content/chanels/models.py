from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Chanel(models.Model):
    id = models.CharField(max_length=12, primary_key=True, editable=False)
    name = models.CharField(max_length=200, unique=True)
    desc = models.CharField(max_length=1000, blank=True)
    img = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    admins = models.ManyToManyField(User, related_name='admin_chanels')
    owner = models.ForeignKey(User, related_name='owner_chanels', on_delete=models.PROTECT)
    subscribers = models.ManyToManyField(User, related_name='subscriptions')
    subscribers_milestones = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    def subs(self):
        return self.subscribers.count()
    def view_url(self):
        return f'/c/{self.id}'
    def editors(self):
        all_editors = []
        all_editors.append(self.owner)
        for admin in self.admins.all():
            all_editors.append(admin)
        return all_editors
