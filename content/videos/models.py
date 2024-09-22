from django.db import models
from django.contrib.auth import get_user_model
from content.chanels.models import Chanel

User = get_user_model()


class Video(models.Model):
    id = models.CharField(max_length=12, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000, blank=True)
    url = models.CharField(max_length=11)
    img = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE, related_name='videos')
    authors = models.ManyToManyField(User, related_name='videos')
    liked_users = models.ManyToManyField(User, related_name='liked_videos')
    likes_milestones = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    def view_url(self):
        return f'/v/{self.id}'
    def editors(self):
        return self.authors.all()
    def likes(self):
        return self.liked_users.count()

class Comment(models.Model):
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='answers')
    liked_users = models.ManyToManyField(User, related_name='liked_comments')
    likes_milestones = models.IntegerField(default=0)

    def __str__(self):
        return str(self.text)[:20]

    def likes(self):
        return self.liked_users.count()

    def editors(self):
        return [self.author]


