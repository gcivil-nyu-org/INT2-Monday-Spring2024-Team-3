# admin.py

from .models import Event, Review, UserEvent, Chat, BlockedUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Event)
admin.site.register(Review)
admin.site.register(UserEvent)
admin.site.register(Chat)
# Your UserProfile import here


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email")

    actions = ["block_users", "unblock_users"]

    def block_users(self, request, queryset):
        for user in queryset:
            BlockedUser.objects.create(
                user=user, reason="Your reason for blocking goes here"
            )
            user.is_active = False
            user.save()

    block_users.short_description = "lock"

    def unblock_users(self, request, queryset):
        blocked_users = BlockedUser.objects.filter(user__in=queryset)
        blocked_users.delete()
        queryset.update(is_active=True)

    unblock_users.short_description = "unlock"


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
