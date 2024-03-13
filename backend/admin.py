# admin.py
from .models import Event, Review, UserEvent, Chat, BlockedUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils import timezone

# Register models
admin.site.register(Event)
admin.site.register(Review)
admin.site.register(UserEvent)
admin.site.register(Chat)


# Register BlockedUser model with custom admin options
class BlockedUserAdmin(admin.ModelAdmin):
    list_display = ("user", "reason", "blocked_at", "end_at")


admin.site.register(BlockedUser, BlockedUserAdmin)


# Register CustomUserAdmin with custom user management options
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_blocked",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email")

    actions = ["block_users", "unblock_users"]

    def is_blocked(self, obj):
        return obj.blockeduser is not None

    is_blocked.boolean = True
    is_blocked.short_description = "Blocked"

    def block_users(self, request, queryset):
        end_at_input = input("Enter end date and time (YYYY-MM-DD HH:MM:SS): ")
        end_at = timezone.datetime.strptime(end_at_input, "%Y-%m-%d %H:%M:%S")
        reason = input("Suspend reason: ")
        for user in queryset:
            BlockedUser.objects.create(user=user, reason=reason, end_at=end_at)
            user.is_active = False
            user.save()

    block_users.short_description = "Suspend"

    def unblock_users(self, request, queryset):
        blocked_users = BlockedUser.objects.filter(user__in=queryset)
        for blocked_user in blocked_users:
            if blocked_user.end_at <= timezone.now():
                blocked_user.delete()
        queryset.update(is_active=True)

    unblock_users.short_description = "Resume"


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
