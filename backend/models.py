import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


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


class SuspendedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    suspended_at = models.DateTimeField(auto_now_add=True)
    unsuspended_at = models.DateTimeField(null=True, blank=True)
    is_suspended = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def unsuspend_user(self):
        self.is_suspended = False
        self.user.save()
        self.delete()


class BannedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    banned_at = models.DateTimeField(auto_now_add=True)
    unban_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def unban_user(self):
        self.user.is_active = True
        self.user.save()
        self.delete()
