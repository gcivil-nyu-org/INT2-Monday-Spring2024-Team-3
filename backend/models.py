import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=1000, default="Category not defined")
    description = models.TextField(blank=True)
    open_date = models.DateField(default=datetime.date.today)
    close_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=1000)
    external_link = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    avg_rating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title


# Review model
class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


# UserEvent model for likes/saves
class UserEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved = models.BooleanField(default=False)


# Chat model
class Chat(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_chats"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_chats"
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class BannedUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="banned_user"
    )
    banned_until = models.DateTimeField(null=True, blank=True)

    def unban_user(self):
        self.banned_until = None
        self.save()

    def extend_ban(self, days):
        if self.banned_until is not None:
            self.banned_until += timezone.timedelta(days=days)
        else:
            self.banned_until = timezone.now() + timezone.timedelta(days=days)
        self.save()
