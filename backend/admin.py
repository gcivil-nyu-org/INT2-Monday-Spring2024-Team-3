# admin.py

from django.contrib import admin
from .models import Event, Review, UserEvent, Chat, User
from django.contrib.auth.admin import UserAdmin


admin.site.register(Event)
admin.site.register(Review)
admin.site.register(UserEvent)
admin.site.register(Chat)
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass
