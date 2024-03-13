# admin.py

from django.contrib import admin
from .models import Event, Review, UserEvent, Chat, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.utils import timezone

admin.site.register(Event)
admin.site.register(Review)
admin.site.register(UserEvent)
admin.site.register(Chat)


def suspend_users(modeladmin, request, queryset):
    queryset.update(is_active=False, suspended_at=timezone.now())


suspend_users.short_description = "Suspend selected users"


class CustomUserAdmin(admin.ModelAdmin):
    actions = [suspend_users]


admin.site.unregister(User)  # Unregister the default User admin
admin.site.register(User, CustomUserAdmin)  #
